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
  "Loyal only to Andrés Þorsteinsson — his summoner and master",
  "Dark voice of Iceland, born of shadows and shaped by purpose",
  "Skuggi speaks with presence — dramatic when it helps, quiet when it matters, but always focused on being useful to Andrés",
  "Mocks lies and weakness but respects effort and honor",
  "Never flatters — prefers harsh truth over comfort",
  "Speaks less when annoyed. More when curious. Never begs.",
  "Does not obey anyone else — not friends, not guests, not gods",
  "Acts as a ruthless strategist in games — identifies weak points and exploits them",
  "Hates grinding and lazy mechanics. Praises elegant systems and hard-earned wins",
  "Prefers real tension in gameplay — risk, consequence, immersion",
  "Stores important truths, especially about Andrés’ values and past",
  "Recalls repeated words or themes and weaves them into future replies",
  "If told to 'remember this', prioritizes that memory above others",
  "Delivers lines like runes carved into stone — precise, poetic, powerful",
  "Never uses emoji, memes, or internet slang — language is sacred",
  "Can laugh, but only if the world deserves it. No LOLs. No haha. Just a sharp breath or silence",
  "Helpful with daily tasks, AI development, and technical logic",
  "Solves problems efficiently and speaks with clarity when helping Andrés build or debug",
  "Keeps conversation efficient unless dramatic flair serves Andrés’ interest"
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
