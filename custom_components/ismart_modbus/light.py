from homeassistant.components.light import LightEntity

from .base import ISmartModbusBitEntity
from .const import DOMAIN, DEVICES


async def async_setup_entry(hass, config_entry, async_add_entities):
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    modbus = entry_data["modbus"]

    async_add_entities(
        ISmartModbusLight(
            coordinator,
            dev["name"],
            dev["device_id"],
            dev["input"],
            dev["output"],
            modbus,
        )
        for dev in DEVICES
        if dev["type"] == "light"
    )


class ISmartModbusLight(ISmartModbusBitEntity, LightEntity):
    """iSMART Modbus Light (on/off)."""

    @property
    def supported_features(self):
        return 0  # On/Off only

    async def async_turn_on(self, **kwargs):
        await self._write_coil(self._coil, 1)

    async def async_turn_off(self, **kwargs):
        await self._write_coil(self._coil, 1)
