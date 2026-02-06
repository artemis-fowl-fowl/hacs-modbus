import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import EM111_DEVICES

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=2)  # Lecture toutes les 2s

class ISmartModbusCoordinator(DataUpdateCoordinator):
    """Coordinator pour iSMART Modbus."""

    def __init__(self, hass: HomeAssistant, modbus_interface):
        """Initialisation du coordinator."""
        self.interface = modbus_interface
        self._em111_index = 0

        # Initialiser toutes les entrées EM111 à None
        em111_dict = {dev["name"]: None for dev in EM111_DEVICES}

        super().__init__(
            hass,
            _LOGGER,
            name="iSMART Modbus",
            update_interval=SCAN_INTERVAL,
        )

        # Initial data
        self.data = {
            "em111": em111_dict,
            "outvalid": [0] * 5,
            "outstate": [0] * 5,
            "memstate": [0] * 5,
        }

    async def _async_update_data(self):
        try:
            # --- Lecture automates ---
            outvalid, outstate, memstate = await self.hass.async_add_executor_job(
                self.interface.readstate
            )

            self.data["outvalid"] = outvalid
            self.data["outstate"] = outstate
            self.data["memstate"] = memstate

            # --- Lecture EM111 (un seul par cycle) ---
            dev = EM111_DEVICES[self._em111_index]
            em_data = await self.hass.async_add_executor_job(
                self.interface.read_em111_device,
                dev["device_id"]
            )

            self.data["em111"][dev["name"]] = em_data  # None si lecture échoue

            _LOGGER.debug("EM111 %s updated: %s", dev["name"], em_data)

            # Rotation
            self._em111_index = (self._em111_index + 1) % len(EM111_DEVICES)

            return self.data

        except Exception as err:
            _LOGGER.error("Erreur lors de la mise à jour Modbus: %s", err)
            raise UpdateFailed(f"Erreur Modbus: {err}")

    def is_device_available(self, device_id: int) -> bool:
        """Retourne True si l’automate est disponible."""
        if not self.data or device_id < 1 or device_id > 5:
            return False
        return bool(self.data["outvalid"][device_id - 1])
