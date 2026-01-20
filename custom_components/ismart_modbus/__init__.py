"""Intégration iSMART Modbus pour Home Assistant."""

import logging
from typing import Final

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_SERIAL_PORT, CONF_BAUDRATE, CONF_TIMEOUT
from .modbus_interface import ModbusInterface
from .coordinator import ISmartModbusCoordinator

_LOGGER: logging.Logger = logging.getLogger(__name__)

# Plates-formes supportées : switches, binary sensors (feedback), covers (template)
PLATFORMS: Final = [Platform.SWITCH]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configurer l'intégration à partir d'une config entry."""
    _LOGGER.info(f"Initialisation iSMART Modbus: {entry.title}")
    
    hass.data.setdefault(DOMAIN, {})
    
    # Créer l'interface Modbus
    modbus_interface = ModbusInterface(
        port=entry.data[CONF_SERIAL_PORT],
        baudrate=entry.data.get(CONF_BAUDRATE, 38400),
        timeout=entry.data.get(CONF_TIMEOUT, 0.03)
    )
    
    # Connecter à l'interface
    if not await modbus_interface.async_connect():
        _LOGGER.error("Impossible de se connecter à l'interface Modbus")
        return False
    
    # Créer le coordinateur pour le polling périodique
    coordinator = ISmartModbusCoordinator(hass, modbus_interface)
    
    # Première mise à jour
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = {
        "config": entry.data,
        "modbus": modbus_interface,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Décharger l'intégration."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        entry_data = hass.data[DOMAIN].pop(entry.entry_id)
        # Déconnecter l'interface Modbus
        if "modbus" in entry_data:
            entry_data["modbus"].disconnect()
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Recharger l'intégration."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

