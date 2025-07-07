import os
import time
import subprocess
import asyncio
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write as wav_write
from edge_tts import Communicate
import whisper
from utils.gpt import get_response
from utils.memory import load_memory, save_memory

print("\033[92m✔ FULL VOICE.PY LOADED - CLEANUP PATCH ACTIVE\033[0m")

SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
whisper_model = whisper.load_model("base")
memory = load_memory()
chat_history = []

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
    except Exception as e:
        print("Failed to delete temp files:", e)

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
    duration = 1  # seconds
    recording = []

    def callback(indata, frames, time_info, status):
        recording.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='int16', callback=callback):
        sd.sleep(int(duration * 1000))

    if recording:
        audio = np.concatenate(recording, axis=0)
        return np.linalg.norm(audio)
    return 500  # fallback default

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

        if not listening:
            print('🤫 (Skuggi is on hold...)')
            continue

        print(f'🔊 You said: {transcript}')
        chat_history.append({"role": "user", "content": transcript})
        reply = await get_response(transcript, chat_history, memory)
        chat_history.append({"role": "assistant", "content": reply})

        await speak(reply)
        save_memory(memory)
























        save_memory(memory)






















