import logging
from homeassistant.helpers.update_coordinator import CoordinatorEntity

_LOGGER = logging.getLogger(__name__)


class ISmartModbusBase(CoordinatorEntity):
    """Base class for all iSMART Modbus entities."""

    def __init__(self, coordinator, name, device_id, modbus_interface):
        super().__init__(coordinator)
        self._name = name
        self._device_id = device_id
        self._modbus = modbus_interface

    @property
    def name(self):
        return self._name

    @property
    def available(self):
        return self.coordinator.is_device_available(self._device_id)

    async def _write_coil(self, coil, value: int = 1):
        """Write a Modbus coil and refresh state."""
        try:
            if await self.hass.async_add_executor_job(self._modbus.writecoil_device, self._device_id, coil, value) == True:
                await self.coordinator._async_update_ismart(self._device_id)        # Refresh partiel pour cet automate
                self.coordinator.async_update_listeners()                           # Force la mise à jour dans home assistant
            else:
                _LOGGER.error("Modbus write failed on %s", self._name)
        except Exception as e:
            _LOGGER.error("Modbus error on %s: %s", self._name, e)

    @staticmethod
    def decode_input(string):
        """Decode input like I1 / X1 to Modbus coil address."""
        if string.startswith("I"):
            return 0x0550 + int(string[1:]) - 1
        if string.startswith("X"):
            return 0x0560 + int(string[1:]) - 1
        raise ValueError(f"Invalid input '{string}'")

    @staticmethod
    def decode_output(string):
        """Decode output like Q1 / Y1 to bit position."""
        if string.startswith("Q"):
            return int(string[1:]) - 1
        if string.startswith("Y"):
            return 8 + int(string[1:]) - 1
        raise ValueError(f"Invalid output '{string}'")

class ISmartModbusBitEntity(ISmartModbusBase):
    """Base class for bit-based Modbus entities."""
    def __init__(self, coordinator, name, device_id, input, output, modbus_interface):
        super().__init__(coordinator, name, device_id, modbus_interface)
        self._coil = self.decode_input(input)
        self._bit_position = self.decode_output(output)

    @property
    def is_on(self):
        state = self.coordinator.get_bit(self._device_id, "outputs", self._bit_position)
        return bool(state)