"""Coordinator for iSMART Modbus integration."""
import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=2)  # Lecture toutes les 10 secondes pour éviter saturation RS485


class ISmartModbusCoordinator(DataUpdateCoordinator):
    """Coordinator to manage data updates from Modbus."""

    def __init__(self, hass: HomeAssistant, modbus_interface):
        """Initialize the coordinator."""
        self.modbus_interface = modbus_interface
        _LOGGER.warning(f"Init coordinator 26")
        super().__init__(hass, _LOGGER, name="iSMART Modbus", update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Fetch data from Modbus."""
        #_LOGGER.debug(f"update_data is executed")
        #_LOGGER.info(f"update_data is executed")
        #_LOGGER.warning(f"update_data is executed")
        try:
            # Lecture d'état sur les 5 automates
            outvalid, outstate, memstate = await self.hass.async_add_executor_job(
                self.modbus_interface.readstate
            )
            
            _LOGGER.warning(
                "Modbus state updated - valid: %s, outstate: %s, memstate: %s",
                outvalid, outstate, memstate
            )
            
            return {
                "outvalid": outvalid,
                "outstate": outstate,
                "memstate": memstate,
            }
            
        except Exception as err:
            _LOGGER.error("Error fetching Modbus data: %s", err)
            raise UpdateFailed(f"Error communicating with Modbus: {err}")

    def get_bit(self, device_id: int, address: int, bit_position: int) -> bool | None:
        """
        Get a bit from coordinator data.
        
        Args:
            device_id: Slave ID (1-5)
            address: Register address
            bit: Bit position in the register (1-32)
            
        Returns:
            True if bit 1, False if 0, None if unavailable
        """
        if not self.data:
            return None
        
        # Vérifier que l'automate est valide
        if device_id not in [1,2,3,4,5]:        ### A améliorer!!!!
            return None
        
        # Je ne comprends pas trop cette méthode. outvalid est crée dans modbus interface, mais data n'apparait nul part.
        # Est-ce que self.data.get est un fonction spécifique qui permet d'aller chercher la variable outvalid ??
        outvalid = self.data.get("outvalid", [0, 0, 0, 0, 0])
        
        if not outvalid[device_id - 1]:
            _LOGGER.warning(f"get_bit {device_id}.{bit_position} returns None")
            return None
        
        # Récupérer l'état des sorties (outstate)
        # ICI ON TRICHE ON NE PREND PAS EN COMPTE L'ADDRESSE DU REGISTRE
        outstate = self.data.get("outstate", [0, 0, 0, 0, 0])
        state_word = outstate[device_id - 1]
        
        if bit_position not in range (0,16):
            _LOGGER.warning(f"bit position {bit_position} out of range (0,16) for state reading")
            return None
        
        # Tester le bit
        bit_value = (state_word >> bit_position) & 1
        _LOGGER.warning(f"get_bit {device_id}.{bit_position} returns {bool(bit_value)}")
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
