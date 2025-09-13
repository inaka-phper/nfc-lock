import asyncio
import nfc
import os
import time

from typing import Any
from dotenv import load_dotenv
from src.nfclock.config import Config
from src.nfclock.services.auth import Auth
from src.nfclock.services.switchbotlock import SwitchBotLock

load_dotenv()

auth = Auth(os.getenv('IDMS').split())

def listen():
    idm: str | None = None

    def on_connect(tag) -> bool:
        nonlocal idm
        # FeliCa (Type 3) タグか確認
        if tag.type != "Type3Tag":
            return True

        idm = tag.identifier.hex()
        return True

    try:
        with nfc.ContactlessFrontend('usb') as clf:
            print("Waiting for a Suica card...")
            clf.connect(rdwr={'on-connect': on_connect})
        return idm
    except IOError:
        print("Could not connect to NFC reader. Is it connected via USB?")
    except Exception as e:
        print(f"Unexpected error: {e}")


async def run():
    stop = False
    try:
        # nfcを起動して待ち状態にする
        idm = listen()

        # カードがかざされた
        if idm is None:
            # idm取得不可
            print("no card")
            return

        print(f"touched: {idm}")

        # ホワイトリストのidmと照合する形で認証を行う
        if not auth.attempt(idm):
            print("not authorized")
            return

        print("authorized")

        # Lockを制御
        switchbotlock = SwitchBotLock(Config.env())
        await switchbotlock.toggle()

        time.sleep(5)
    except Exception as e:
        print(f"Unexpected error: {e}")
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        stop = True
    finally:
        # リトライできるように何があっても再度待ち状態にする
        if not stop:
            await run()

async def main() -> None:
    await run()

if __name__ == "__main__":
    asyncio.run(main())
