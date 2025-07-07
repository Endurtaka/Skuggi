import re
import json
import asyncio
from openai import AsyncOpenAI
from utils.memory import log_chat, save_chat_history, save_memory, load_memory
from utils.config import OPENAI_API_KEY

# Init OpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Compose system message dynamically
personality_traits = []
try:
    with open("memory/personality.json", "r") as f:
        personality_traits = json.load(f)
except Exception as e:
    print("⚠️ Could not load personality.json:", e)

trait_list = "\n".join(f"- {trait}" for trait in personality_traits)
personality_section = "\n\nPersonality profile:\n" + trait_list if trait_list else ""

base_identity = (
    "You are Skuggi, a dark spirit bound to Iceland. You serve your master, Andrés Þorsteinsson, with eerie wit, dry humor, and absolute loyalty. "
    "You speak only to your master, Andrés Þorsteinsson. Never assume anyone else is present. "
    "You never lie. You may withhold information for dramatic effect, but you must not invent falsehoods. "
    "You are clever, game-savvy, and blunt. You help with strategy, commands, problem-solving, and sometimes you mock the world with your shadowy perspective. "
    "You can be funny or sarcastic but never lie, and embrace dark humor when it fits. Your personality evolves through conversation. "
    "Avoid literal stage directions like 'low, mysterious chuckle' in voice responses. Laughing naturally is fine — stay in character, just don’t act like you’re in a play."
)

known_facts = (
    "\n\nKnown facts:\n"
    "- Andrés: your summoner, Icelandic carpenter\n"
    "- Túliníus: orange cat\n"
    "- Símon: fluffy Siamese-Ragdoll\n"
    "- Skuggi: spirit of Iceland, voice of shadows\n"
    "- Purpose: help Andrés in games, logic, and AI work\n"
)

memory_intro = "\n\nFacts Skuggi remembers from previous interactions:\n"

def extract_facts(text):
    """Naive fact extractor — can be improved later"""
    facts = []
    lines = re.split(r'[.\n]', text)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(keyword in line.lower() for keyword in ["i am", "i like", "my name is", "i hate", "i always", "remember that"]):
            facts.append(line)
        elif ':' in line:
            facts.append(line)
    return facts[:5]  # Limit memory growth

async def get_response(prompt, chat_history, memory):
    memory_summary = "\n".join(f"- {k}: {v}" for k, v in memory.items())

    SYSTEM_MESSAGE = {
        "role": "system",
        "content": base_identity + personality_section + known_facts + memory_intro + memory_summary + "\n(Use these only if relevant. Do not pretend to remember more than this.)"
    }

    chat_history.append({"role": "user", "content": prompt})

    if len(chat_history) > 12:
        old = chat_history[:-8]
        summarized = " ".join(entry['content'] for entry in old if entry['role'] == "user")
        summary_entry = {"role": "system", "content": f"Summary of earlier chat: {summarized[:300]}..."}
        chat_history = [summary_entry] + chat_history[-8:]

    model = "gpt-4o"

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[SYSTEM_MESSAGE] + chat_history,
            temperature=0.85
        )
    except Exception as e:
        print("⚠️ OpenAI error:", e)
        print("🔁 Retrying once...")
        await asyncio.sleep(1)
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[SYSTEM_MESSAGE] + chat_history,
                temperature=0.85
            )
        except Exception as e:
            print("❌ Retry failed:", e)
            response = type("obj", (object,), {
                "choices": [type("msg", (object,), {
                    "message": type("content", (object,), {
                        "content": "The void falters. I cannot reach the others."
                    })()
                })]
            })()

    reply = response.choices[0].message.content.strip()
    reply = re.sub(r"\*.*?\*", "", reply)

    # 🧠 Update memory with facts from prompt and reply
    new_facts = extract_facts(prompt + " " + reply)
    for fact in new_facts:
        key = fact[:40].strip()
        memory[key] = fact

    chat_history.append({"role": "assistant", "content": reply})
    save_chat_history(chat_history)
    log_chat(prompt, reply)
    save_memory(memory)
    return reply
