"""Switches Modbus pour iSMART."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, DEVICE_TO_SLAVE, ALL_ROOMS, CONF_PORT, CONF_BAUDRATE, CONF_METHOD

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Ajouter les switches depuis la config."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    config = data["config"]
    
    port = config.get(CONF_PORT)
    baudrate = config.get(CONF_BAUDRATE)
    method = config.get(CONF_METHOD, "rtu")
    
    entities = []
    
    # Pour chaque salle et ses appareils
    for room_name, room_devices in data["rooms"].items():
        for device_key, device_info in room_devices.items():
            device_id = device_info["device"]
            slave = DEVICE_TO_SLAVE.get(device_id, device_id + 1)
            coil = device_info["coil"]
            name = device_info["name"]
            entity_id = f"switch_{room_name}_{device_key}"
            
            entities.append(
                ISmartModbusSwitch(
                    name=name,
                    unique_id=f"ismart_{entity_id}",
                    room=room_name,
                    device_key=device_key,
                    slave=slave,
                    coil=coil,
                    port=port,
                    baudrate=baudrate,
                    method=method,
                    hass=hass,
                )
            )
    
    if entities:
        async_add_entities(entities)
        _LOGGER.info(f"Ajouté {len(entities)} switches iSMART")


class ISmartModbusSwitch(SwitchEntity):
    """Switch Modbus iSMART."""

    def __init__(
        self,
        name: str,
        unique_id: str,
        room: str,
        device_key: str,
        slave: int,
        coil: int,
        port: str,
        baudrate: int,
        method: str,
        hass: HomeAssistant,
    ) -> None:
        """Initialiser le switch."""
        self._name = name
        self._unique_id = unique_id
        self._room = room
        self._device_key = device_key
        self._slave = slave
        self._coil = coil
        self._port = port
        self._baudrate = baudrate
        self._method = method
        self._hass = hass
        self._is_on = False
        self._available = False

    @property
    def name(self) -> str:
        """Nom du switch."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Identifiant unique."""
        return self._unique_id

    @property
    def is_on(self) -> bool:
        """État du switch."""
        return self._is_on

    @property
    def available(self) -> bool:
        """Disponibilité (basée sur la dernière tentative)."""
        return self._available

    @property
    def icon(self) -> str:
        """Icône."""
        if "volet" in self._name.lower() or "vr" in self._device_key.lower():
            return "mdi:window-shutter"
        elif "lit" in self._name.lower():
            return "mdi:bed"
        else:
            return "mdi:lightbulb" if self._is_on else "mdi:lightbulb-outline"

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Allumer le switch."""
        # Appeler modbus.write_coil via un service HA
        await self._hass.services.async_call(
            "modbus",
            "write_coil",
            {
                "hub": "ismart",
                "unit": self._slave,
                "address": self._coil,
                "value": True,
            },
        )
        self._is_on = True
        self._available = True
        self.async_write_ha_state()
        _LOGGER.debug(f"Switch {self._name} (slave={self._slave}, coil={hex(self._coil)}) allumé")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Éteindre le switch."""
        # Pulse off ou vrai OFF selon le device
        await self._hass.services.async_call(
            "modbus",
            "write_coil",
            {
                "hub": "ismart",
                "unit": self._slave,
                "address": self._coil,
                "value": False,
            },
        )
        self._is_on = False
        self._available = True
        self.async_write_ha_state()
        _LOGGER.debug(f"Switch {self._name} (slave={self._slave}, coil={hex(self._coil)}) éteint")

    async def async_update(self) -> None:
        """Mettre à jour l'état (optionnel, basé sur verify)."""
        # En mode simple, pas de lecture auto. L'état se fait via UI.
        # Si tu veux du feedback, ajoute un binary_sensor dédié.
        pass
