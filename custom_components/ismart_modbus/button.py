"""Button platform for iSMART Modbus."""
import logging
from homeassistant.components.button import ButtonEntity

from .base import ISmartModbusBase
from .const import DOMAIN, DEVICES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    modbus = entry_data["modbus"]
    entities = [
        ISmartModbusButton(coordinator, dev["name"], dev["device_id"], dev["input"], modbus)
        for dev in DEVICES if dev["type"] == "button"
    ]
    async_add_entities(entities)


class ISmartModbusButton(ISmartModbusBase, ButtonEntity):

    def __init__(self, coordinator, name: str, device_id: int, input, modbus):
        super().__init__(coordinator, name, device_id, modbus)
        self._attr_unique_id = f"button_{name.lower()}"
        self._coil = self.decode_input(input)   
        self._attr_name = name

    async def async_press(self) -> None:
        await self._write_coil(self._coil)

    @property
    def icon(self):
        return "mdi:gesture-tap-button"
    