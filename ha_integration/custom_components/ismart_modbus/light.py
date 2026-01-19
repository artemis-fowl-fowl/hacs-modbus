"""Lumières pour iSMART Modbus."""

import json
import logging
from typing import Any, Dict, List, Optional

import aiohttp
from homeassistant.components.light import LightEntity, LightEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_HOST,
    CONF_PORT,
    CONF_LIGHTS,
    DEFAULT_PORT,
    DEFAULT_TIMEOUT,
    DOMAIN,
    STATE_OFF,
    STATE_ON,
    STATE_ERROR,
)

_LOGGER = logging.getLogger(__name__)


class ISmartModbusLight(LightEntity):
    """Représente une lumière iSMART Modbus."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        port: int,
        name: str,
        device: int,
        index: int,
        addr: str,
    ):
        """Initialiser la lumière."""
        self.hass = hass
        self._host = host
        self._port = port
        self._attr_name = name
        self._device = device
        self._index = index
        self._addr = addr.lower()
        self._is_on = False
        self._available = True
        self._session = None
        self._attr_unique_id = f"ismart_{host}_{device}_{index}"
        self._attr_supported_features = LightEntityFeature.TRANSITION

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Allumer la lumière."""
        try:
            # Envoyer la commande writeCoil pour allumer
            url = f"http://{self._host}:{self._port}/writeCoil[{self._device},{self._addr},1]"
            session = async_get_clientsession(self.hass)
            async with session.get(url, timeout=DEFAULT_TIMEOUT) as resp:
                if resp.status == 200:
                    self._is_on = True
                    self._available = True
                    _LOGGER.debug(f"Lumière {self._attr_name} allumée")
                else:
                    self._available = False
                    _LOGGER.error(f"Erreur lors de l'allumage: {resp.status}")
        except Exception as err:
            self._available = False
            _LOGGER.error(f"Erreur lors de l'allumage: {err}")

        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Éteindre la lumière."""
        try:
            # Envoyer la commande writeCoil pour éteindre
            url = f"http://{self._host}:{self._port}/writeCoil[{self._device},{self._addr},0]"
            session = async_get_clientsession(self.hass)
            async with session.get(url, timeout=DEFAULT_TIMEOUT) as resp:
                if resp.status == 200:
                    self._is_on = False
                    self._available = True
                    _LOGGER.debug(f"Lumière {self._attr_name} éteinte")
                else:
                    self._available = False
                    _LOGGER.error(f"Erreur lors de l'extinction: {resp.status}")
        except Exception as err:
            self._available = False
            _LOGGER.error(f"Erreur lors de l'extinction: {err}")

        self.async_write_ha_state()

    async def async_update(self) -> None:
        """Mettre à jour l'état de la lumière."""
        try:
            # Récupérer l'état avec getState
            url = f"http://{self._host}:{self._port}/getState"
            session = async_get_clientsession(self.hass)
            async with session.get(url, timeout=DEFAULT_TIMEOUT) as resp:
                if resp.status == 200:
                    data = await resp.text()
                    self._parse_state(data)
                    self._available = True
                else:
                    self._available = False
                    _LOGGER.error(f"Erreur lors de la récupération de l'état: {resp.status}")
        except Exception as err:
            self._available = False
            _LOGGER.error(f"Erreur lors de la mise à jour: {err}")

    def _parse_state(self, data: str) -> None:
        """Parser la réponse de getState."""
        try:
            # Exemple de réponse: "[validState0,validState1,...][outState0,outState1,...][memState0,memState1,...]"
            # Remplacer les ";" par "]["
            data = data.replace("][", ";")
            data = data.replace("[", "")
            data = data.replace("]", "")

            lists = data.split(";")

            if len(lists) >= 3:
                valid_state = list(map(int, lists[0].split(",")))
                out_state = list(map(int, lists[1].split(",")))
                mem_state = list(map(int, lists[2].split(",")))

                # Vérifier si la donnée est valide
                if self._device <= len(valid_state):
                    if valid_state[self._device - 1] == 0:
                        self._is_on = False
                        _LOGGER.debug(f"Lumière {self._attr_name}: donnée non valide")
                    else:
                        # Si l'index < 100, lire dans outState sinon dans memState
                        if self._index < 100:
                            bit_value = (
                                out_state[self._device - 1] >> self._index
                            ) & 0x1
                        else:
                            bit_value = (
                                mem_state[self._device - 1]
                                >> (self._index - 100)
                            ) & 0x1

                        self._is_on = bit_value == 1
                        _LOGGER.debug(
                            f"Lumière {self._attr_name}: {self._is_on}"
                        )
        except Exception as err:
            _LOGGER.error(f"Erreur lors du parsing de l'état: {err}")

    @property
    def is_on(self) -> bool:
        """Retourner l'état de la lumière."""
        return self._is_on

    @property
    def available(self) -> bool:
        """Retourner si la lumière est disponible."""
        return self._available


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurer les lumières à partir d'une config entry."""
    host = entry.data.get(CONF_HOST)
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    lights_config = entry.data.get(CONF_LIGHTS, [])

    lights: List[ISmartModbusLight] = []

    if isinstance(lights_config, str):
        try:
            lights_config = json.loads(lights_config)
        except json.JSONDecodeError:
            _LOGGER.error("Configuration des lampes invalide")
            return

    for light_config in lights_config:
        light = ISmartModbusLight(
            hass,
            host,
            port,
            light_config.get("name", "Lumière"),
            light_config.get("device", 1),
            light_config.get("index", 0),
            light_config.get("addr", "0x2C00"),
        )
        lights.append(light)

    async_add_entities(lights)

    # Mettre à jour les états au démarrage
    for light in lights:
        await light.async_update()
