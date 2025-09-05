from typing import Any, Coroutine

from switchbot.devices import lock
from switchbot.const import SwitchbotModel
from switchbot.devices.lock import SwitchbotLock
from switchbot.discovery import GetSwitchbotDevices

from src.nfclock.config import Config

class SwitchBotLock:
    def __init__(self, config: Config):
        self.config = config

    async def searchDevice(self) -> SwitchbotLock:
        devices = await GetSwitchbotDevices().get_locks()
        device = devices[self.config.ble_mac].device
        return lock.SwitchbotLock(device, self.config.key_id, self.config.enc_key, model=SwitchbotModel.LOCK_PRO)

    async def lock(self) -> bool:
        target = await self.searchDevice()
        return await target.lock()

    async def unlock(self) -> bool:
        target = await self.searchDevice()
        return await target.unlock()
