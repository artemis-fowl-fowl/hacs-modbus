"""Button platform for iSMART Modbus."""
import logging
from homeassistant.components.button import BinarySensorEntity

from .base import ISmartModbusBase
from .const import DOMAIN, DEVICES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = entry_data["coordinator"]
    modbus = entry_data["modbus"]
    entities = [
        ISmartModbusButton(coordinator, dev["name"], dev["device_id"], dev["output"], modbus)
        for dev in DEVICES if dev["type"] == "sensor"
    ]
    async_add_entities(entities)


class ISmartModbusBinarySensor(ISmartModbusBase, BinarySensorEntity):

    def __init__(self, coordinator, name: str, device_id: int, output, modbus):
        super().__init__(coordinator, name, device_id, modbus)
        self._attr_unique_id = f"button_{name.lower()}"
        self._attr_name = name
        self._state_flag = output

    @property
    def is_on(self):
        return bool(self.coordinator.get_bit(self._device_id, self._state_flag))
    