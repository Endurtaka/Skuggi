import asyncio
from utils.voice import local_loop

if __name__ == "__main__":
    print("🧠 Skuggi has risen — local mic mode.")
    print("Say 'disconnect' to banish him.")
    asyncio.run(local_loop())
