"""Switch platform for iSMART Modbus."""
import logging
from homeassistant.components.switch import SwitchEntity

from .base import ISmartModbusBitEntity
from .const import DOMAIN, DEVICES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    modbus = entry_data["modbus"]

    entities = [
        ISmartModbusSwitch(coordinator, dev["name"], dev["device_id"], dev["input"], dev["output"], modbus)
        for dev in DEVICES
        if dev["type"] == "switch"
    ]

    async_add_entities(entities)

class ISmartModbusSwitch(ISmartModbusBitEntity, SwitchEntity):
    """iSMART Modbus Switch."""

    def __init__(self, coordinator, name: str, device_id: int, input_reg, output_reg, modbus):
        super().__init__(coordinator, name, device_id, input_reg, output_reg, modbus)
        ### Normalement il faudrait corriger le nom (supprimmer {device_id})
        self._attr_unique_id = f"switch_{device_id}_{name.lower()}"
        self._attr_name = name

    async def async_turn_on(self, **kwargs):
        if self.is_on:
            return
        await self._write_coil(self._coil)

    async def async_turn_off(self, **kwargs):
        if not self.is_on:
            return
        await self._write_coil(self._coil)

    @property
    def icon(self):
        return "mdi:lightbulb-on" if self.is_on else "mdi:lightbulb-outline"