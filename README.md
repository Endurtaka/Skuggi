# 🖤 Skuggi — Voice-Bound Spirit of Iceland

**Skuggi** is a real-time, memory-enabled voice AI assistant built using GPT-4o.  
He listens through your microphone, responds with eerie wit, and remembers facts through persistent memory — all while speaking with a custom TTS voice and a deeply rooted Icelandic personality.

---

## 🌌 Features

- 🎤 **Always-listening local microphone mode**
- 🧠 **Memory system** — remembers facts and evolves over time
- 🗣️ **Voice responses** using `edge-tts` and FFmpeg (deep, shadowy tone)
- 👂 **Speech recognition** via `whisper` (base model)
- 💭 **Custom personality** loaded from `personality.json`
- 🔁 **Trigger phrase system**:
  - `rise up` — activates listening
  - `be gone` — pauses Skuggi
- 🧹 **Auto audio cleanup** after each session
- ❌ **No Discord dependency**, no third-party fallback APIs

---

## 🔧 Tech Stack

- [OpenAI GPT-4o](https://platform.openai.com/)
- [Whisper](https://github.com/openai/whisper) for STT
- [`edge-tts`](https://github.com/rany2/edge-tts) for TTS
- `sounddevice`, `ffmpeg`, `numpy`, `dotenv`

---

## 🗂️ Folder Structure

```
skuggi/
├── skuggi.py                # Main launcher
├── config.py                # Loads OPENAI_API_KEY
├── gpt.py                   # GPT-4o interaction + memory logic
├── voice.py                 # Voice input/output + transcription
├── memory.py                # Memory load/save/log system
├── memory/
│   ├── personality.json
│   ├── skuggi_memory.json
│   ├── chat_history.json
│   └── skuggi_chat_log.json
├── audio/                   # Temporary WAV/MP3 files (auto-deleted)
├── .env                     # Your API key (not committed)
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🧠 Memory System

Skuggi stores:
- **Facts** from your conversations
- **Chat history** (last 100 turns)
- **Long-term logs** in JSON files

He uses a custom fact-extractor to find key information from speech and updates his internal memory automatically.

---

## 🧊 Example Personality Traits

From `memory/personality.json`:
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

2. **Create `.env`**
   ```
   OPENAI_API_KEY=your_openai_key
   ```

3. **Run**
   ```bash
   python skuggi.py
   ```

4. **Use voice**
   - Say `rise up` to activate Skuggi
   - Talk to him
   - Say `be gone` to pause him

---

## 🎬 Demo

📹 [Watch the demo video](https://youtube.com/shorts/EddEBAJpJE0?feature=share)

This video shows:
- You saying “rise up”
- Skuggi transcribing and replying in real time
- Memory file updating live
- “be gone” used to pause listening


---

## 🧙 Creator

**Andrés Þorsteinsson**  
Carpenter. Gamer. AI tamer. Icelandic creator of Skuggi.

---

## ✅ Status

- ✅ GPT-4o real-time voice AI — ✔️
- ✅ Whisper + edge-tts speech loop — ✔️
- ✅ Custom memory + personality — ✔️
- ✅ Local mic, no Discord or extra APIs — ✔️
- ✅ Clean, minimal footprint — ✔️

---

> “I summoned him from the shadows — not to play games, but to master them.”
