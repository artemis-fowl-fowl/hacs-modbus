"""Coordinator for iSMART Modbus integration (one EM111 per cycle)."""

import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import SCAN_INTERVAL, ISMART_DEVICES, EM111_DEVICES

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
            "em111": {dev["name"]: None for dev in EM111_DEVICES},  # On crée un disctionnaire pour chaque EM111 avec son nom comme clé et None comme valeur initiale
            "ismart": {i: None for i in ISMART_DEVICES},            # On crée un disctionnaire pour chaque automate iSMART avec son device_id comme clé et None comme valeur initiale
        }

    ### La gestion des exception est bancale au niveau du projet.
    ### Il est nécessaire que chaque fonction enrichisse l'exception puis la fasse remontée pour tracer correctement l'erreur dans les logs et éviter les erreurs silencieuses.
    
    async def _async_update_ismart(self, device_id):
        """Fetch data for a specific iSMART device."""
        try:
            ismart_data = await self.hass.async_add_executor_job(self.modbus_interface.read_ismart, device_id)
            self.data["ismart"][device_id] = ismart_data  # None si lecture échoue
            _LOGGER.info(f"Partial update for iSMART {device_id} -> outputs: {ismart_data['outputs']}, m_registers: {ismart_data['m_registers']}")
        except Exception as err:
            _LOGGER.error(f"Error fetching data for iSMART {device_id}: {err}")
            raise  # Relance l'exception pour permettre à _async_update_data de la gérer

    async def _async_update_data(self):
        """Fetch data from all automates and one EM111 per cycle."""
        try:
            # Mise à jour des automates iSMART
            for device_id in ISMART_DEVICES:
                await self._async_update_ismart(device_id)  # Appel de la fonction factorisée pour chaque automate

            # --- Lecture EM111 (un seul par cycle) ---
            if EM111_DEVICES:  # On vérifie si la liste EM111_DEVICES existe et n'est pas vide
                dev = EM111_DEVICES[self._em111_index]
                em_data = await self.hass.async_add_executor_job(self.modbus_interface.read_em111_device, dev["device_id"])
                self.data["em111"][dev["name"]] = em_data  # None si lecture échoue
                # Rotation
                self._em111_index = (self._em111_index + 1) % len(EM111_DEVICES)

            return self.data

        except Exception as err:
            _LOGGER.error("Error fetching Modbus data: %s", err)
            raise UpdateFailed(f"Modbus failure: {err}")

    """
    # --- Méthodes utilitaires pour les automates (inchangées) ---
    def get_bit(self, device_id: int, register: str, bit_position: int) -> bool | None:
        """Get the state of a specific bit in the given register for a specific device."""
        # Vérification de l'existence des données pour le device_id
        if device_id not in self.data["ismart"]:
            return None
        # Récupération des données du device_id
        device_data = self.data["ismart"][device_id]
        if not device_data or register not in device_data:
            return None
        # Vérification de la validité de la position du bit
        if bit_position not in range(16):
            return None
        # Récupération de la valeur du registre et extraction du bit
        register_value = device_data[register]
        return bool((register_value >> bit_position) & 1)
    """
        
    @staticmethod
    def decode_bit_name(string: str):
        """Return the bit register and position."""
        try:
            if string.startswith("Q"):
                return "outputs", int(string[1:]) - 1
            if string.startswith("Y"):
                return "outputs", int(string[1:]) + 7
            if string.startswith("M"):
                return "m_registers", int(string[1:]) - 1
        except ValueError:
            raise ValueError(f"Invalid bit_name '{string}': Unable to resolve bit position")

        raise ValueError(f"Invalid bit_name '{string}': Unable to resolve register type")

    def get_bit2(self, device_id: int, bit_name: str) -> bool | None:
        """Get the state of a specific bit in the given register for a specific device."""
        # Vérification de l'existence des données pour le device_id
        if device_id not in self.data["ismart"]:
            return None
        
        device_data = self.data["ismart"][device_id]                # Récupération des données du device_id
        register, bit_position = self.decode_bit_name(bit_name)     # Décodage du bit_name pour obtenir le registre et la position du bit

        if not device_data or register not in device_data:
            return None
        # Vérification de la validité de la position du bit
        if bit_position not in range(16):
            return None
        # Récupération de la valeur du registre et extraction du bit
        register_value = device_data[register]
        return bool((register_value >> bit_position) & 1)

    # La fonction s'appelle is_device_available pourtant elle ne concerne que les Ismart, pas les EM111.
    # Il y a un problème d'architecture globale dans le projet.
    def is_device_available(self, device_id: int) -> bool:
        # Retourne True si les données pour le device_id existent et sont valides, sinon False
        if device_id not in self.data["ismart"]:
            return False
        if not self.data["ismart"][device_id]:
            return False
        return True

