import logging
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

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
    def decode_input(string: str) -> int:
        """Return the Ismart coil address of an input string like "I1" or "X1"."""
        if string is None:
            return None
        offset = int(string[1:], 16) - 1        
        if string.startswith("I"):
            return 0x0550 + offset
        elif string.startswith("X"):
            return 0x0560 + offset
        if string.startswith("M"):
            if offset < 16:
                return 0x0540 + offset          # Ismart v2 compatibility
            return 0x2B80 + offset              # Ismart v3 only ???
        if string.startswith("N"):
            if offset < 16:
                return 0x0590 + offset          # Ismart v2 compatibility
            return 0x2BC0 + offset              # Ismart v3 only ???
        if string.startswith("B"):             
            return 0x2D00 + offset              # Ismart v3 only ???     
        else:
            raise ValueError(f"Input string '{string}' is invalid.")


    # Le device_info est utilisé par Home Assistant pour regrouper les entités par appareil dans l'interface utilisateur.
    # On ne veux pas ce ça
    #@property
    #def device_info(self):
    #    return {
    #        "identifiers": {(DOMAIN, self._device_id)},
    #        "name": self._name,
    #        "manufacturer": "IMO",
    #        "model": "iSMART",
    #    }

class ISmartModbusBitEntity(ISmartModbusBase):
    """Base class for bit-based Modbus entities."""
    def __init__(self, coordinator, name, device_id, input, output, modbus_interface):
        super().__init__(coordinator, name, device_id, modbus_interface)
        self._coil = self.decode_input(input)
        self._state_flag = output

    @property
    def is_on(self):
        return bool(self.coordinator.get_bit(self._device_id, self._state_flag))