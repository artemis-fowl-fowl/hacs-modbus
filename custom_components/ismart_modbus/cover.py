"""Shutter platform for iSMART Modbus."""
import logging
from homeassistant.components.cover import CoverEntity, CoverDeviceClass, CoverState
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
    """Set up iSMART Modbus covers."""
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    modbus_interface = entry_data["modbus"]
    coordinator = entry_data["coordinator"]

    entities = [
        ISmartModbusCover(
            coordinator=coordinator,
            name=dev["name"],
            device_id=dev["device_id"],
            up=dev["up"],
            down=dev["down"],
            opening=dev["opening"],
            closing=dev["closing"],
            opened=dev.get("opened"),
            closed=dev.get("closed"),
            modbus_interface=modbus_interface,
        )
        for dev in COVER_DEVICES
    ]

    async_add_entities(entities)


class ISmartModbusCover(CoordinatorEntity, CoverEntity):
    """Representation of an iSMART Modbus cover (shutter)."""

    _attr_device_class = CoverDeviceClass.SHUTTER

    def __init__(
        self,
        coordinator,
        name: str,
        device_id: int,
        up: str,
        down: str,
        opening: str,
        closing: str,
        opened: str | None = None,
        closed: str | None = None,
        modbus_interface=None,
    ):
        """Initialize the cover."""
        super().__init__(coordinator)
        self._name = name
        self._device_id = device_id
        self._modbus = modbus_interface

        # Coils pour commandes
        self._up_coil = self.decode_input(up)
        self._down_coil = self.decode_input(down)

        # Flags obligatoires
        self._opening_flag_pos = self.decode_output(opening)
        self._closing_flag_pos = self.decode_output(closing)

        # Flags optionnels
        self._opened_flag_pos = self.decode_output(open
