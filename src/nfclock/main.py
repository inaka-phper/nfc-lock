import asyncio

from src.nfclock.config import Config
from src.nfclock.services.switchbotlock import SwitchBotLock


async def main() -> None:
    switchbotlock = SwitchBotLock(Config.env())
    await switchbotlock.unlock()
    print("unlocked")

if __name__ == "__main__":
    asyncio.run(main())
