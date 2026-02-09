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
        ISmartGarage(
            coordinator=coordinator,
            name=dev["name"],
            device_class=dev["type"],
            device_id=dev["device_id"],
            move=dev["move"],
            opened=dev["opened"],
            closed=dev["closed"],
            modbus_interface=modbus_interface,
        )
        if dev["type"] == "garage" else

        ISmartGate(
            coordinator=coordinator,
            name=dev["name"],
            device_class=dev["type"],
            device_id=dev["device_id"],
            move=dev["move"],
            lock=dev["lock"],
            partial=dev["partial"],
            closed=dev["closed"],
            modbus_interface=modbus_interface,
        )
        if dev["type"] == "gate" else

        ISmartModbusCover(
            coordinator=coordinator,
            name=dev["name"],
            device_class=dev["type"],
            device_id=dev["device_id"],
            up=dev["up"],
            down=dev["down"],
            opening=dev["opening"],
            closing=dev["closing"],
            opened=dev["opened"],
            closed=dev["closed"],
            modbus_interface=modbus_interface,
        )
        for dev in COVER_DEVICES if "type" in dev and dev["type"]
        ]

    async_add_entities(entities)


class ISmartModbusCover(CoordinatorEntity, CoverEntity):
    """Representation of an iSMART Modbus cover (shutter)."""

    def __init__(
        self,
        coordinator,
        name: str,
        device_class: str,
        device_id: int,
        up: str,
        down: str,
        opening: str,
        closing: str,
        opened: str,
        closed: str,
        modbus_interface=None,
    ):
        """Initialize the cover."""
        super().__init__(coordinator)
        self._attr_unique_id = f"cover_{name.lower()}"
        self._attr_name = name
        self._name = name
        self._device_id = device_id
        self._modbus = modbus_interface

        _attr_device_class = CoverDeviceClass.SHUTTER

        # Coils pour commandes
        self._up_coil = self.decode_input(up)
        self._down_coil = self.decode_input(down)
        # Flags obligatoires
        self._opening_flag = opening
        self._closing_flag = closing
        # Flags optionnels
        self._opened_flag = opened
        self._closed_flag = closed
        
    @staticmethod
    def decode_input(string: str) -> int:
        """Return the Ismart coil address of an input string like "I1" or "X1"."""
        if string is None:
            return None
        if string.startswith("I"):
            return 0x0550 + int(string[1:]) - 1
        elif string.startswith("X"):
            return 0x0560 + int(string[1:]) - 1
        else:
            raise ValueError(f"Input string '{string}' is invalid.")

    async def _write_coil(self, coil, value: int = 1):
        """Write a Modbus coil and refresh state."""
        try:
            if await self.hass.async_add_executor_job(self._modbus.writecoil_device, self._device_id, coil, value) == True:
                await self.coordinator._async_update_ismart(self._device_id)        # Refresh partiel pour cet automate
                self.coordinator.async_update_listeners()                           # Force la mise à jour dans home assistant
            else:
                _LOGGER.error("Modbus write failed on %s", self._name)
        except Exception as e:
            _LOGGER.error("Modbus error on %s: %s", self._name, e)

    @property
    def name(self) -> str:
        return self._name

    @property
    def unique_id(self) -> str:
        return f"ismart_cover_{self._name.lower()}"

    @property
    def is_opening(self) -> bool:
        return bool(self.coordinator.get_bit(self._device_id, self._opening_flag))

    @property
    def is_closing(self) -> bool:
        return bool(self.coordinator.get_bit(self._device_id, self._closing_flag))
    
    @property
    def is_open(self) -> bool:
        return bool(self.coordinator.get_bit(self._device_id, self._opened_flag))

    @property
    def is_closed(self) -> bool:
        return bool(self.coordinator.get_bit(self._device_id, self._closed_flag))

    @property
    def state(self):
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
    def available(self) -> bool:
        return self.coordinator.is_device_available(self._device_id)

    @property
    def icon(self) -> str | None:
        if self.is_opening or self.is_closing:
            return "mdi:window-shutter-cog"
        if self.is_closed:
            return "mdi:window-shutter"
        if self.is_open:
            return "mdi:window-shutter-open"
        return "mdi:window-shutter-alert"

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        await self._write_coil(self._up_coil)

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        await self._write_coil(self._down_coil)

    async def async_stop_cover(self, **kwargs):
        """Stop the cover by pulsing the active coil."""
        coil = None
        if self.is_opening:
            coil = self._up_coil
        elif self.is_closing:
            coil = self._down_coil

        if coil is not None:
            await self._write_coil(coil)


class ISmartGarage(ISmartModbusCover):
    """Representation of an iSMART Modbus garage door."""

    def __init__(self, coordinator, name, device_class, device_id, move, opened, closed, modbus_interface):
        """Initialize the garage door."""
        super().__init__(coordinator, name, device_class, device_id, None, None, None, None, opened, closed, modbus_interface)
        self._move_coil = self.decode_input(move)
        self._last_direction = None
        _attr_device_class = CoverDeviceClass.GARAGE
        _LOGGER.warning("Initialisation garage")

    async def async_open_cover(self, **kwargs):
        """Open the garage door."""
        if self.is_open or self.is_opening:
            return
        await self._write_coil(self._move_coil)
        #if (await self._write_coil(self._up_coil) == True):
        self._last_direction = "up"
        #LOGGER.warning("Ouverture garage")
        await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs):
        """Close the garage door."""
        if self.is_closed or self.is_closing:
            return
        await self._write_coil(self._move_coil)
        #if (await self._write_coil(self._up_coil) == True):
        self._last_direction = "down"
        #_LOGGER.warning("Fermeture garage")
        await self.coordinator.async_request_refresh()

    @property
    def is_opening(self) -> bool:
        opened = bool(self.coordinator.get_bit(self._device_id, self._opened_flag))
        closed = bool(self.coordinator.get_bit(self._device_id, self._closed_flag))
        moving = not (opened or closed)
        _LOGGER.warning(f"is_opening computation, opened = {opened}, closed = {closed}, moving = {moving}, last_direction = {self._last_direction}")
        return bool(moving and self._last_direction == "up")

    @property
    def is_closing(self) -> bool:
        opened = bool(self.coordinator.get_bit(self._device_id, self._opened_flag))
        closed = bool(self.coordinator.get_bit(self._device_id, self._closed_flag))
        moving = not (opened or closed)
        #_LOGGER.warning(f"is_opening computation, opened = {opened}, closed = {closed}, moving = {moving}, last_direction = {self._last_direction}")
        return bool(moving and self._last_direction == "down")

    # A vérifier !!!!!!!
    @property
    def device_class(self) -> str:
        """Return the class of this device."""
        return "garage"
    
class ISmartGate(ISmartModbusCover):
    """Representation of an iSMART Modbus gate."""

    def __init__(self, coordinator, name, device_class, device_id, move, lock, partial, closed, modbus_interface):
        """Initialize the gate"""
        super().__init__(coordinator, name, device_class, device_id, None, None, None, None, None, closed, modbus_interface)
        self._move_coil = self.decode_input(move)
        self._lock_coil = self.decode_input(lock)
        self._partial_coil = self.decode_input(partial)
        self._state = None
        _attr_device_class = CoverDeviceClass.GARAGE
        _LOGGER.warning("Initialisation garage")

    async def async_open_cover(self, **kwargs):
        """Open the gate."""
        if self.is_open or self.is_opening:
            return
        await self._write_coil(self._move_coil)
        self._last_state = "opening"
        await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs):
        """Close the garage door."""
        if self.is_closed or self.is_closing:
            return
        await self._write_coil(self._move_coil)
        self._last_state = "closing"
        await self.coordinator.async_request_refresh()

    @property
    def is_open(self) -> bool:
        moving = bool(self.coordinator.get_bit(self._device_id, self._moving_flag))
        
        is_open = not moving and not self.is_closed
        if is_open:
            self._last_state = "opened"
        else:
            self._last_state = "closed"
        return not moving and not self.is_closed

    @property
    def is_opening(self) -> bool:
        moving = bool(self.coordinator.get_bit(self._device_id, self._moving_flag))
        opening = moving and self._last_state in ["opened", "opening"]
        self._last_state == "opening"
        return opening

    @property
    def is_closing(self) -> bool:
        moving = bool(self.coordinator.get_bit(self._device_id, self._moving_flag))
        closing = moving and self._last_state not in ["opened", "opening"]
        self._last_state == "closing"
        return closing

    # A vérifier !!!!!!!
    @property
    def device_class(self) -> str:
        """Return the class of this device."""
        return "gate"