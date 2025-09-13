from typing import Any, Coroutine
from switchbot import LockStatus
from switchbot.devices import lock
from switchbot.const import SwitchbotModel
from switchbot.devices.lock import SwitchbotLock
from switchbot.discovery import GetSwitchbotDevices
from src.nfclock.config import Config

class SwitchBotLock:
    def __init__(self, config: Config):
        self.config = config
        self._validate_config()

    def _validate_config(self) -> None:
        if not self.config:
            raise Exception("Config not found.")
        if not self.config.ble_mac or not isinstance(self.config.ble_mac, str):
            raise Exception("BLE_MAC is missing.")
        if not self.config.key_id or not isinstance(self.config.key_id, str):
            raise Exception("KEY_ID is missing.")
        if not self.config.enc_key or not isinstance(self.config.enc_key, str):
            raise Exception("ENC_KEY is missing.")

    async def searchDevice(self) -> SwitchbotLock:
        # Config 検証は __init__ で実施済み
        devices = await GetSwitchbotDevices().get_locks()

        # デバイス探索を安全に
        info = devices.get(self.config.ble_mac)
        if info is None:
            raise Exception(f"Device not found for BLE_MAC: {self.config.ble_mac}")
        device = info.device
        return lock.SwitchbotLock(
            device,
            self.config.key_id.strip(),
            self.config.enc_key.strip(),
            model=SwitchbotModel.LOCK_PRO
        )

    async def lock(self) -> bool:
        target = await self.searchDevice()
        return await target.lock()

    async def unlock(self) -> bool:
        target = await self.searchDevice()
        return await target.unlock()

    async def toggle(self) -> bool:
        commands = {
            LockStatus.LOCKED: self.unlock,
            LockStatus.UNLOCKED: self.lock
        }
        target = await self.searchDevice()
        info = await target.get_basic_info()

        try:
            return await commands[info["status"]]()
        except KeyError:
            raise Exception("Status not found.")
