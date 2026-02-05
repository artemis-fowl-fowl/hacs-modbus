"""Coordinator for iSMART Modbus integration."""
import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import time

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=2)  # Lecture toutes les 10 secondes pour éviter saturation RS485

# EM111 parameters
START_ADDRESS = 0x04
REGISTER_COUNT = 14

class ISmartModbusCoordinator(DataUpdateCoordinator):
    """Coordinator to manage data updates from Modbus."""

    def __init__(self, hass: HomeAssistant, modbus_interface):
        """Initialize the coordinator."""
        self.modbus_interface = modbus_interface

        self._em111_units = [10, 11, 12]
        self._em111_index = 0
        self._em111_data: dict[int, dict | None] = {uid: None for uid in self._em111_units}
        
        super().__init__(hass, _LOGGER, name="iSMART Modbus", update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        try:
            # --- Lecture automates (TOUJOURS) ---
            outvalid, outstate, memstate = await self.hass.async_add_executor_job(
                self.modbus_interface.readstate
            )

            time.sleep(0.05)
            await self.hass.async_add_executor_job(self.modbus_interface.readEM111)
         
            """
            # --- Lecture EM111 (UN SEUL PAR CYCLE) ---
            unit_id = self._em111_units[self._em111_index]

            try:
                em_data = await self.read_em111(unit_id)
                self._em111_data[unit_id] = em_data
                _LOGGER.debug("EM111 %s updated: %s", unit_id, em_data)
            except Exception as err:
                self._em111_data[unit_id] = None
                _LOGGER.warning("EM111 %s unavailable: %s", unit_id, err)

            # Rotation
            self._em111_index = (self._em111_index + 1) % len(self._em111_units)
            """

            return {
                "outvalid": outvalid,
                "outstate": outstate,
                "memstate": memstate,
                "em111": dict(self._em111_data),
            }

        except Exception as err:
            _LOGGER.error("Error fetching Modbus automates data: %s", err)
            raise UpdateFailed(f"Automate Modbus failure: {err}")


    def get_bit(self, register: str, device_id: int, bit_position: int) -> bool | None:
        """
        Get a bit from coordinator data.
        
        Args:
            device_id: Slave ID (1-5)
            address: Register address
            bit: Bit position in the register (1-32)
            
        Returns:
            True if bit 1, False if 0, None if unavailable
        """
        if register not in ("outstate", "memstate"):
            _LOGGER.warning(f"get_bit called with invalid register: {register}")
            return None
        
        if not self.data:
            _LOGGER.warning(f"get_bit {register}.{device_id}.{bit_position} returns None because data is None")
            return None
        
        outvalid = self.data.get("outvalid")
        if not isinstance(outvalid, (list, tuple)):
            _LOGGER.warning(f"get_bit {register}.{device_id}.{bit_position} returns None because outvalid is invalid")
            return None
        
        index = device_id - 1
        if not 0 <= index < len(outvalid):
            _LOGGER.warning(f"get_bit {register}.{device_id}.{bit_position} returns None because device_id is out of range")
            return None
        
        if not outvalid[index]:
            _LOGGER.warning(f"get_bit {register}.{device_id}.{bit_position} returns None because device is not valid")
            return None
        
        states = self.data.get(register)
        if not isinstance(states, (list, tuple)):
            _LOGGER.warning(f"get_bit {register}.{device_id}.{bit_position} returns None because states is invalid")
            return None
        
        if index >= len(states):
            _LOGGER.warning(f"get_bit {register}.{device_id}.{bit_position} returns None because index out of range")
            return None

        state_word = states[index]  # Récupérer l'état des sorties (outstate) ou mémoires (memstate) correspondant à l'automate
        
        if bit_position not in range (0,16):
            _LOGGER.warning(f"bit position {bit_position} out of range (0,16) for state reading")
            return None
        
        # Tester le bit
        bit_value = (state_word >> bit_position) & 1
        _LOGGER.debug(f"get_bit {register}.{device_id}.{bit_position} returns {bool(bit_value)}")
        return bool(bit_value)

    def get_coil_state(self, device_id: int, coil: int) -> bool | None:
        """
        Get the state of a specific coil from coordinator data.
        
        Args:
            device_id: Slave ID (1-5)
            coil: Coil address (e.g., 0x2C02)
            
        Returns:
            True if coil is ON, False if OFF, None if unavailable
        """
        if not self.data:
            return None
        
        # Vérifier que l'automate est valide
        if device_id < 1 or device_id > 5:
            return None
        
        outvalid = self.data.get("outvalid", [0, 0, 0, 0, 0])
        if not outvalid[device_id - 1]:
            return None
        
        # Récupérer l'état des sorties (outstate)
        outstate = self.data.get("outstate", [0, 0, 0, 0, 0])
        state_word = outstate[device_id - 1]
        
        # Calculer le bit correspondant à la bobine
        # Les coils 0x2C00-0x2C17 correspondent aux bits 0-23
        coil_offset = coil - 0x2C00
        
        if coil_offset < 0 or coil_offset > 23:
            _LOGGER.warning("Coil 0x%04X out of range for state reading", coil)
            return None
        
        # Tester le bit
        bit_value = (state_word >> coil_offset) & 1
        return bool(bit_value)

    def is_device_available(self, device_id: int) -> bool:
        """Check if a device is available."""
        if not self.data:
            return False
        
        if device_id < 1 or device_id > 5:
            return False
        
        outvalid = self.data.get("outvalid", [0, 0, 0, 0, 0])
        return bool(outvalid[device_id - 1])

    async def read_em111(self, unit_id: int) -> dict:
        registers = await self.hass.async_add_executor_job(
            self.modbus_interface.read_holding_registers,
            unit_id,
            START_ADDRESS,
            REGISTER_COUNT,
        )

        power = (registers[0] <<16 + registers[1]) / 10
        energy = (registers[14] <<16 + registers[15]) / 10

        return {
            "power": power / 10,
            "energy": energy / 10,
        }

