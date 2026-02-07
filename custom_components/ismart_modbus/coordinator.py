"""Coordinator for iSMART Modbus integration (one EM111 per cycle)."""

import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import SCAN_INTERVAL, EM111_DEVICES

_LOGGER = logging.getLogger(__name__)

class ISmartModbusCoordinator(DataUpdateCoordinator):
    """Coordinator to manage data updates from Modbus."""

    def __init__(self, hass: HomeAssistant, modbus_interface):
        """Initialize the coordinator."""
        self.modbus_interface = modbus_interface
        self._em111_index = 0
        super().__init__(hass, _LOGGER, name="iSMART Modbus", update_interval=timedelta(seconds=SCAN_INTERVAL))

        # Initial data
        self.data = {
            "em111": {dev["name"]: None for dev in EM111_DEVICES},
            "ismart": {i: None for i in [1,2,3,4,5]},
            "outvalid": [0, 0, 0, 0, 0],
            "outstate": [0, 0, 0, 0, 0],
            "memstate": [0, 0, 0, 0, 0],
        }

    async def _async_update_data(self):
        """Fetch data from automates and one EM111 per cycle."""
        try:
            # --- Lecture automates ---
            outvalid, outstate, memstate = await self.hass.async_add_executor_job(self.modbus_interface.readstate)
            self.data["outvalid"] = outvalid
            self.data["outstate"] = outstate
            self.data["memstate"] = memstate
            
            # Pour chacun des 5 automates
            for i in range(0, 2):
                ismart_data = await self.hass.async_add_executor_job(self.modbus_interface.read_ismart, i + 1)         # i + 1 est le device address. ON peut imaginer plus tard que celui-ci serait issu d'ailleurs
                self.data["ismart"][i + 1] = ismart_data  # None si lecture échoue
                if i == 0:
                    _LOGGER.warning(f"outputs : {ismart_data['outputs']}, m_registers : {ismart_data['m_registers']}")
            
            # --- Lecture EM111 (un seul par cycle) ---
            if EM111_DEVICES:   # On vérifie si la liste EM111_DEVICES existe et n'est pas vide pour éviter une division par zéro
                dev = EM111_DEVICES[self._em111_index]
                em_data = await self.hass.async_add_executor_job(self.modbus_interface.read_em111_device, dev["device_id"])
                self.data["em111"][dev["name"]] = em_data  # None si lecture échoue
                #LOGGER.debug("EM111 %s updated: %s", dev["name"], em_data)
                # Rotation
                self._em111_index = (self._em111_index + 1) % len(EM111_DEVICES)

            return self.data

        except Exception as err:
            _LOGGER.error("Error fetching Modbus data: %s", err)
            raise UpdateFailed(f"Modbus failure: {err}")

    # --- Méthodes utilitaires pour les automates (inchangées) ---
    def get_bit(self, register: str, device_id: int, bit_position: int) -> bool | None:
        if register not in ("outstate", "memstate") or not self.data:
            return None
        states = self.data.get(register)
        index = device_id - 1
        if not isinstance(states, (list, tuple)) or index < 0 or index >= len(states):
            return None
        state_word = states[index]
        if bit_position not in range(16):
            return None
        return bool((state_word >> bit_position) & 1)

    def get_coil_state(self, device_id: int, coil: int) -> bool | None:
        if not self.data:
            return None
        if device_id < 1 or device_id > 5:
            return None
        outvalid = self.data.get("outvalid", [0]*5)
        if not outvalid[device_id - 1]:
            return None
        outstate = self.data.get("outstate", [0]*5)
        state_word = outstate[device_id - 1]
        coil_offset = coil - 0x2C00
        if coil_offset < 0 or coil_offset > 23:
            return None
        return bool((state_word >> coil_offset) & 1)

    def is_device_available(self, device_id: int) -> bool:
        if not self.data or device_id < 1 or device_id > 5:
            return False
        outvalid = self.data.get("outvalid", [0]*5)
        return bool(outvalid[device_id - 1])
