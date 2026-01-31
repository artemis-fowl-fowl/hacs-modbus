from homeassistant.components.light import LightEntity
from homeassistant.components.light import ColorMode

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

    _attr_supported_color_modes = {ColorMode.ONOFF}
    _attr_color_mode = ColorMode.ONOFF

    async def async_turn_on(self, **kwargs):
        await self._write_coil(self._coil, 1)

    async def async_turn_off(self, **kwargs):
        await self._write_coil(self._coil, 1)

    @property
    def icon(self):
        return "mdi:lightbulb-on" if self.is_on else "mdi:lightbulb-outline"