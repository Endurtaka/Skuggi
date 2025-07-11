import os
import json

MEMORY_FILE = "memory/skuggi_memory.json"
CHAT_LOG_FILE = "memory/skuggi_chat_log.json"
HISTORY_FILE = "memory/chat_history.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def log_chat(prompt, reply):
    entry = {
        "prompt": prompt,
        "reply": reply
    }
    logs = []
    if os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    logs.append(entry)
    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

def save_chat_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-100:], f, indent=2)
