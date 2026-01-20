"""Switches réseau (HTTP) pour iSMART."""

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    DEVICE_TO_SLAVE,
    ALL_ROOMS,
    CONF_HOST,
    CONF_NET_PORT,
    CONF_MODE,
)

from aiohttp import ClientSession

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Ajouter les switches depuis la config."""
    data = hass.data[DOMAIN][config_entry.entry_id]
    config = data["config"]

    host = config.get(CONF_HOST)
    net_port = config.get(CONF_NET_PORT)
    mode = config.get(CONF_MODE, "legacy")
    
    entities = []
    
    # Pour chaque salle et ses appareils
    for room_name, room_devices in data["rooms"].items():
        for device_key, device_info in room_devices.items():
            device_id = device_info["device"]
            slave = DEVICE_TO_SLAVE.get(device_id, device_id + 1)
            coil = device_info["coil"]
            name = device_info["name"]
            entity_id = f"switch_{room_name}_{device_key}"
            rest_name = device_info.get("rest_name")
            
            entities.append(
                ISmartNetSwitch(
                    name=name,
                    unique_id=f"ismart_{entity_id}",
                    room=room_name,
                    device_key=device_key,
                    slave=slave,
                    coil=coil,
                    rest_name=rest_name,
                    host=host,
                    net_port=net_port,
                    mode=mode,
                    hass=hass,
                )
            )
    
    if entities:
        async_add_entities(entities)
        _LOGGER.info(f"Ajouté {len(entities)} switches iSMART")


class ISmartNetSwitch(SwitchEntity):
    """Switch iSMART via serveur réseau (HTTP)."""

    def __init__(
        self,
        name: str,
        unique_id: str,
        room: str,
        device_key: str,
        slave: int,
        coil: int,
        rest_name: str | None,
        host: str,
        net_port: int,
        mode: str,
        hass: HomeAssistant,
    ) -> None:
        """Initialiser le switch."""
        self._name = name
        self._unique_id = unique_id
        self._room = room
        self._device_key = device_key
        self._slave = slave
        self._coil = coil
        self._host = host
        self._net_port = net_port
        self._mode = mode
        self._hass = hass
        self._rest_name = rest_name
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
        async with ClientSession() as session:
            try:
                if self._mode == "rest":
                    # REST: /api/toggle/<name> (POST) ou /api/volet/<name>/open
                    base = f"http://{self._host}:{self._net_port}"
                    # Déduire la cible REST
                    rest_name = getattr(self, "_rest_name", None)
                    if rest_name is None:
                        # fallback: slug à partir du room
                        rest_name = self._room
                    if "volet_up" in self._device_key:
                        url = f"{base}/api/volet/{rest_name}/open"
                        async with session.post(url, timeout=5) as resp:
                            self._available = resp.status == 200
                    elif "volet_down" in self._device_key:
                        url = f"{base}/api/volet/{rest_name}/close"
                        async with session.post(url, timeout=5) as resp:
                            self._available = resp.status == 200
                    else:
                        url = f"{base}/api/toggle/{rest_name}"
                        async with session.post(url, timeout=5) as resp:
                            self._available = resp.status == 200
                else:
                    # Legacy: /writeCoil[slave,addr,1]
                    url = f"http://{self._host}:{self._net_port}/writeCoil[{self._slave},{self._coil},1]"
                    async with session.get(url, timeout=5) as resp:
                        self._available = resp.status == 200
            except Exception:
                self._available = False
        self._is_on = True
        self._available = True
        self.async_write_ha_state()
        _LOGGER.debug(f"Switch {self._name} (slave={self._slave}, coil={hex(self._coil)}) allumé")

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Éteindre le switch."""
        async with ClientSession() as session:
            try:
                if self._mode == "rest":
                    # REST ne fournit qu'un toggle pour les lumières; on re-toggles
                    base = f"http://{self._host}:{self._net_port}"
                    rest_name = getattr(self, "_rest_name", None)
                    if rest_name is None:
                        rest_name = self._room
                    if "volet_up" in self._device_key:
                        # pas de stop: on renvoie open (idempotence côté automate)
                        url = f"{base}/api/volet/{rest_name}/open"
                        async with session.post(url, timeout=5) as resp:
                            self._available = resp.status == 200
                    elif "volet_down" in self._device_key:
                        url = f"{base}/api/volet/{rest_name}/close"
                        async with session.post(url, timeout=5) as resp:
                            self._available = resp.status == 200
                    else:
                        url = f"{base}/api/toggle/{rest_name}"
                        async with session.post(url, timeout=5) as resp:
                            self._available = resp.status == 200
                else:
                    url = f"http://{self._host}:{self._net_port}/writeCoil[{self._slave},{self._coil},0]"
                    async with session.get(url, timeout=5) as resp:
                        self._available = resp.status == 200
            except Exception:
                self._available = False
        self._is_on = False
        self._available = True
        self.async_write_ha_state()
        _LOGGER.debug(f"Switch {self._name} (slave={self._slave}, coil={hex(self._coil)}) éteint")

    async def async_update(self) -> None:
        """Mettre à jour l'état (optionnel, basé sur verify)."""
        # En mode simple, pas de lecture auto. L'état se fait via UI.
        # Si tu veux du feedback, ajoute un binary_sensor dédié.
        pass
