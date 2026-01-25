"""Shutter platform for iSMART Modbus."""
import logging
from homeassistant.components.cover import CoverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, COVER_DEVICES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up iSMART Modbus switches."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    modbus_interface = entry_data["modbus"]
    coordinator = entry_data["coordinator"]

    entities = []
    for device_info in COVER_DEVICES:
        entities.append(
            ISmartModbusCover(
                coordinator=coordinator,
                name=device_info["name"],
                device_id=device_info["device_id"],
                up_coil=device_info["up_coil"],
                down_coil=device_info["down_coil"],
                up_bit=device_info["up_bit"],
                down_bit=device_info["down_bit"],
                open_bit=device_info["open_bit"],
                closed_bit=device_info["closed_bit"],
                device_class=device_info["device_class"],
                modbus_interface=modbus_interface,
            )
        )

    async_add_entities(entities)


class ISmartModbusCover(CoordinatorEntity, CoverEntity):
    """Representation of an iSMART Modbus Cover."""

    def __init__(self, coordinator, name, device_id, up_coil, down_coil, up_bit, down_bit, open_bit, closed_bit, device_class, modbus_interface):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._name = name
        self._device_id = device_id
        self._up_coil = up_coil
        self._down_coil = down_coil
        self._up_bit = up_bit
        self._down_bit = down_bit
        self._open_bit = open_bit
        self._closed_bit = closed_bit
        self._device_class = device_class
        self._modbus = modbus_interface

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"ismart_{self._device_id}_{self._up_coil}"

    @property
    def is_opening(self):
        """Return true if switch is on."""
        # Récupérer l'état depuis le coordinateur
        state = self.coordinator.get_bit(self._device_id, self._up_bit)
        return state if state is not None else False

    @property
    def is_closing(self):
        """Return true if switch is on."""
        # Récupérer l'état depuis le coordinateur
        state = self.coordinator.get_bit(self._device_id, self._down_bit)
        return state if state is not None else False

    @property
    def is_open(self):
        """Return true if the shutter is up."""
        # Récupérer l'état depuis le coordinateur
        state = self.coordinator.get_bit(self._device_id, self._open_bit)
        return state if state is not None else False

    @property
    def is_closed(self):
        """Return true if the shutter is up."""
        # Récupérer l'état depuis le coordinateur
        state = self.coordinator.get_bit(self._device_id, self._closed_bit)
        return state if state is not None else False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.is_device_available(self._device_id)

    @property
    def icon(self):
        """Return the icon."""
        #if self._device_class == "cover":
        if self.is_opening:
            return "mdi:window-shutter-cog"
        if self.is_closing:
            return "mdi:window-shutter-cog"
        if self.is_closed:
            return "mdi:window-shutter"
        if self.is_open:
            return "mdi:window-shutter-open"
    


    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        try:
            result = await self.hass.async_add_executor_job(
                self._modbus.writecoil_device,
                self._device_id,
                self._up_coil,
                1
            )
            if result == 0:
                _LOGGER.info("Switch %s turned on", self._name)
                # Rafraîchir immédiatement l'état
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error("Failed to turn on %s", self._name)
        except Exception as e:
            _LOGGER.error("Error turning on %s: %s", self._name, e)

    async def async_close_cover(self, **kwargs):
        """Turn the switch off."""
        try:
            result = await self.hass.async_add_executor_job(
                self._modbus.writecoil_device,
                self._device_id,
                self._down_coil,
                1  # Les automates attendent une impulsion (1) meme pour "off"
            )
            if result == 0:
                _LOGGER.info("Switch %s turned off", self._name)
                # Rafraîchir immédiatement l'état
                await self.coordinator.async_request_refresh()
            else:
                _LOGGER.error("Failed to turn off %s", self._name)
        except Exception as e:
            _LOGGER.error("Error turning off %s: %s", self._name, e)
