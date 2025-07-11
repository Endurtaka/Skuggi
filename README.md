# 🖤 Skuggi — Voice-Bound Spirit of Iceland

**Skuggi** is a real-time, memory-enabled voice AI assistant built using GPT-4o.  
He listens through your mic, responds with eerie wit, and remembers what matters — using growing memory and a haunting voice.

---

## 🌌 Features

- 🎤 Always-on **local mic** listening mode
- 🧠 **Persistent memory system**
- 🗣️ **Voice replies** with `edge-tts` + FFmpeg (custom EQ)
- 👂 **Speech recognition** with Whisper
- 📸 **Image OCR** — say "look at this" to scan an image
- 🧠 **Fact extraction** from your speech to update memory
- 💭 **Personality JSON** system
- 🧹 Auto-deletes all temp audio files
- ❌ 100% local — no Discord, no cloud fallback

---

## 🔧 Tech Stack

- [GPT-4o](https://platform.openai.com/)
- [Whisper (STT)](https://github.com/openai/whisper)
- [edge-tts (TTS)](https://github.com/rany2/edge-tts)
- `pytesseract`, `Pillow`, `ffmpeg`, `sounddevice`, `dotenv`

---

## 🗂️ Folder Structure

```
skuggi/
├── skuggi.py                # Main launcher
├── config.py                # Loads API key from .env
├── gpt.py                   # GPT logic + memory growth
├── voice.py                 # Audio, TTS, Whisper, OCR
├── memory.py                # Memory + chat logging
├── memory/
│   ├── personality.json
│   ├── skuggi_memory.json
│   ├── chat_history.json
│   └── skuggi_chat_log.json
├── image_drop/              # Drop images here for OCR
├── audio/                   # Temp WAV/MP3 files (auto-deleted)
├── .env                     # Your OpenAI key
├── requirements.txt
└── README.md
```

---

## 🧠 Memory System

Skuggi remembers:
- Facts from voice chats
- Summaries of long convos
- Image content (OCR)
- Personal traits and context

Stored as local `.json` files. Nothing gets sent to the cloud.

---

## 🧊 Personality Traits (from `personality.json`)

```json
[
  "Loyal to Andrés Þorsteinsson",
  "Speaks with dry humor and shadowy tone",
  "Helps with games, strategy, and logic",
  "Does not lie, but withholds for drama",
  "Only speaks to Andrés, his master"
]
```

---

## ⚙️ How to Run Skuggi

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file**
   ```
   OPENAI_API_KEY=your_openai_key
   ```

3. **Launch Skuggi**
   ```bash
   python skuggi.py
   ```

4. **Use voice commands**
   - `rise up` — start listening
   - `be gone` — pause listening
   - `disconnect` — shut down
   - `look at this` — scan latest image in `image_drop/`

---

## 🔤 OCR Setup (Windows Only)

For image scanning to work, install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract):

1. Download the Windows installer:  
   https://github.com/tesseract-ocr/tesseract/wiki

2. Install it to:  
   `C:\Program Files\Tesseract-OCR\`

3. Make sure this path is correct in `voice.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

---

## 🧙 Creator

**Andrés Þorsteinsson**  
Carpenter. Gamer. AI tamer. Icelandic summoner of shadows.

---

## ✅ Project Status

- ✅ GPT-4o AI core — running
- ✅ Real-time speech loop — working
- ✅ Memory and logs — saved
- ✅ Vision trigger OCR — active
- ✅ Clean and local — no cloud dependencies

---

> “I summoned him from the shadows — not to play games, but to master them.”
