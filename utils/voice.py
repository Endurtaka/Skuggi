import os
import time
import subprocess
import asyncio
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as wav_write
from edge_tts import Communicate
import whisper
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
from utils.gpt import get_response
from utils.memory import load_memory, save_memory

print("\033[92m✔ FULL VOICE.PY LOADED - VISION TRIGGER ACTIVE\033[0m")

SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
whisper_model = whisper.load_model("base")
memory = load_memory()
chat_history = []

IMAGE_DIR = "image_drop"
os.makedirs(IMAGE_DIR, exist_ok=True)

async def speak(text):
    print(f"\U0001F5E3 Skuggi says: {text}")
    tts = Communicate(text=text, voice="en-US-ChristopherNeural")
    await tts.save("tts_output.mp3")

    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", "tts_output.mp3",
            "-af", "aresample=44100,asetrate=44100*0.85,atempo=1.0,firequalizer=gain_entry='entry(100,0);entry(1000,5);entry(3000,3)'",
            "demon_output.wav"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        subprocess.run(["ffplay", "-nodisp", "-autoexit", "demon_output.wav"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print("Playback failed:", e)

    try:
        os.remove("tts_output.mp3")
        os.remove("demon_output.wav")
    except Exception as e:
        print(f"Cleanup error: {e}")

def record_until_silence(threshold):
    buffer = []
    silence_start = None
    start_time = time.time()

    def callback(indata, frames, time_info, status):
        nonlocal buffer, silence_start
        volume_norm = np.linalg.norm(indata) * 10
        buffer.append(indata.copy())

        if volume_norm < threshold:
            if silence_start is None:
                silence_start = time.time()
        else:
            silence_start = None

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16', callback=callback, blocksize=0):
        print("🎤 Listening...")
        while True:
            sd.sleep(100)
            if silence_start and (time.time() - silence_start > 2.5):
                print("🔴 Silence detected.")
                break
            if time.time() - start_time > 120:
                print("⚠️ Max duration reached.")
                break

    audio_data = np.concatenate(buffer, axis=0)
    final_file = "audio/local_input.wav"
    wav_write(final_file, SAMPLE_RATE, audio_data)
    print(f"📄 Saved full audio to {final_file}")
    return final_file

def transcribe_audio(filename):
    try:
        print(f"🔎 Transcribing {filename}...")
        result = whisper_model.transcribe(filename)
        return result['text'].strip()
    except Exception as e:
        print("Transcription failed:", e)
        return ""

def get_ambient_level():
    duration = 1
    recording = []

    def callback(indata, frames, time_info, status):
        recording.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16', callback=callback):
        sd.sleep(int(duration * 1000))

    if recording:
        audio = np.concatenate(recording, axis=0)
        return np.linalg.norm(audio)
    return 500

def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang="isl+eng").strip()
        if len(text) < 10:
            return ""
        return text
    except Exception as e:
        print(f"❌ Failed to process {image_path}: {e}")
        return ""

async def image_vision_trigger():
    images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not images:
        await speak("I see nothing. The folder is empty.")
        return

    latest = sorted(images)[-1]
    full_path = os.path.join(IMAGE_DIR, latest)
    print(f"🖼️ Looking at: {latest}")

    text = extract_text_from_image(full_path)
    if not text:
        await speak("There's nothing I can read from that.")
    else:
        memory[f"Seen: {latest}"] = text
        chat_history.append({"role": "user", "content": text})
        reply = await get_response(f"From image: {text}", chat_history, memory)

        if any(phrase in reply.lower() for phrase in [
            "this article covers various topics",
            "concise summary",
            "as you can see",
            "summarizing"
        ]):
            reply = "This image contains mostly structural or repetitive content. Nothing important was found."

        chat_history.append({"role": "assistant", "content": reply})
        await speak(reply)

    save_memory(memory)

async def local_loop():
    listening = True
    disconnect_commands = ["disconnect", "be gone", "shut down"]
    while True:
        volume = get_ambient_level()
        threshold = min(volume * 2.5, 15000)
        print(f"🛋 Ambient level: {volume:.2f}")

        filename = record_until_silence(threshold)
        transcript = transcribe_audio(filename)
        if not transcript:
            continue

        lower = transcript.lower().strip()

        if 'be gone' in lower:
            listening = False
            print('🔇 Skuggi has gone silent.')
            continue

        if 'rise up' in lower:
            listening = True
            print('🔊 Skuggi is listening again.')
            continue

        if 'look at this' in lower:
            await image_vision_trigger()
            continue

        if not listening:
            print('🤫 (Skuggi is on hold...)')
            continue

        print(f'🔊 You said: {transcript}')
        chat_history.append({"role": "user", "content": transcript})
        reply = await get_response(transcript, chat_history, memory)
        chat_history.append({"role": "assistant", "content": reply})

        await speak(reply)
        save_memory(memory)

if __name__ == "__main__":
    asyncio.run(local_loop())
