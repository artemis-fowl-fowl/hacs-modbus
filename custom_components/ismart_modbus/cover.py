"""Shutter platform for iSMART Modbus."""
import logging
from homeassistant.components.cover import CoverEntity, CoverDeviceClass, CoverState
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, COVER_DEVICES
from .base import ISmartModbusBitEntity  # base commune avec switch/light

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
            opening=dev.get("opening"),
            closing=dev.get("closing"),
            opened=dev.get("opened"),
            closed=dev.get("closed"),
            modbus_interface=modbus_interface,
        )
        for dev in COVER_DEVICES
    ]

    async_add_entities(entities)


class ISmartModbusCover(ISmartModbusBitEntity, CoverEntity):
    """Representation of an iSMART Modbus cover (shutter)."""

    _attr_device_class = CoverDeviceClass.SHUTTER  # par défaut, peut être changé

    def __init__(
        self, coordinator, name, device_id, up, down,
        opening=None, closing=None, opened=None, closed=None,
        modbus_interface=None
    ):
        """Initialize the cover."""
        super().__init__(coordinator, name, device_id, modbus_interface)
        # Coils pour commandes
        self._up_coil = self.decode_input(up)
        self._down_coil = self.decode_input(down)

        # Flags pour état
        self._opening_flag_pos = self.decode_output(opening) if opening else self._up_coil
        self._closing_flag_pos = self.decode_output(closing) if closing else self._down_coil
        self._opened_flag_pos = self.decode_output(opened) if opened else self._opening_flag_pos
        self._closed_flag_pos = self.decode_output(closed) if closed else self._closing_flag_pos

    @property
    def is_opening(self):
        """Return True if the cover is opening."""
        state = self.coordinator.get_bit("outstate", self._device_id, self._opening_flag_pos)
        return bool(state)

    @property
    def is_closing(self):
        """Return True if the cover is closing."""
        state = self.coordinator.get_bit("outstate", self._device_id, self._closing_flag_pos)
        return bool(state)

    @property
    def is_open(self):
        """Return True if cover is open."""
        state = self.coordinator.get_bit("memstate", self._device_id, self._opened_flag_pos)
        return bool(state)

    @property
    def is_closed(self):
        """Return True if cover is closed."""
        state = self.coordinator.get_bit("memstate", self._device_id, self._closed_flag_pos)
        return bool(state)

    @property
    def state(self):
        """Return the HA cover state."""
        if self.is_opening:
            return CoverState.OPENING
        if self.is_closing:
            return CoverState.CLOSING
        if self.is_closed:
            return CoverState.CLOSED
        if self.is_open:
            return CoverState.OPEN
        return None

    @property
    def icon(self) -> str | None:
        """Return the icon for the cover."""
        if self.is_opening or self.is_closing:
            return "mdi:window-shutter-cog"
        if self.is_closed:
            return "mdi:window-shutter"
        if self.is_open:
            return "mdi:window-shutter-open"
        return "mdi:window-shutter-alert"

    async def async_open_cover(self, **kwargs):
        await self._write_coil(self._up_coil)

    async def async_close_cover(self, **kwargs):
        await self._write_coil(self._down_coil)

    async def async_stop_cover(self, **kwargs):
        """Stop the cover by pulsing the active coil."""
        coil = None
        if self.is_opening:
            coil = self._up_coil
        elif self.is_closing:
            coil = self._down_coil

        if coil is None:
            return  # pas de mouvement → rien à faire

        await self._write_coil(coil)
