"""Intégration iSMART Modbus pour Home Assistant."""

import logging
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, DEVICE_TO_SLAVE, ALL_ROOMS

_LOGGER: logging.Logger = logging.getLogger(__name__)

# Plates-formes supportées : switches, binary sensors (feedback), covers (template)
PLATFORMS: Final = [Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurer l'intégration à partir d'une config entry."""
    _LOGGER.info(f"Initialisation iSMART Modbus: {entry.title}")
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "config": entry.data,
        "device_to_slave": DEVICE_TO_SLAVE,
        "rooms": ALL_ROOMS,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharger l'intégration."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Recharger l'intégration."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

