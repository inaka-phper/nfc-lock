from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

BLE_MAC=os.getenv('BLE_MAC')
KEY_ID=os.getenv('KEY_ID')
ENC_KEY=os.getenv('ENC_KEY')

@dataclass(frozen=True)
class Config:
    ble_mac: str
    key_id: str
    enc_key: str

    @staticmethod
    def env() -> "Config":
        return Config(
            ble_mac=BLE_MAC,
            key_id=KEY_ID,
            enc_key=ENC_KEY
        )
