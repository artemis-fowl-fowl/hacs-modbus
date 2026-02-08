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
        for dev in COVER_DEVICES
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
        self._attr_unique_id = f"cover_{device_id}_{name.lower()}"
        self._attr_name = name
        self._name = name
        self._device_id = device_id
        self._modbus = modbus_interface

        if device_class == 'garage':
            _attr_device_class = CoverDeviceClass.GARAGE
        else:
            _attr_device_class = CoverDeviceClass.SHUTTER

        # Coils pour commandes
        self._up_coil = self.decode_input(up)
        self._down_coil = self.decode_input(down)

        # Flags obligatoires
        self._opening_flag = opening
        self._closing_flag = closing
        # A supprimer
        self._opening_flag_pos = self.decode_output(opening)
        self._closing_flag_pos = self.decode_output(closing)

        # Flags optionnels
        self._opened_flag = opened
        self._closed_flag = closed
        
        # A supprimer
        self._opened_flag_pos = self.decode_output(opened) if opened else self._opening_flag_pos
        self._closed_flag_pos = self.decode_output(closed) if closed else self._closing_flag_pos


    @staticmethod
    def decode_input(string: str) -> int:
        """Return the Ismart coil address of an input string like "I1" or "X1"."""
        if string.startswith("I"):
            return 0x0550 + int(string[1:]) - 1
        elif string.startswith("X"):
            return 0x0560 + int(string[1:]) - 1
        else:
            raise ValueError(f"Input string '{string}' is invalid.")

    #### Methode à sortir de cette classe pour être utilisée dans les autres entités (switch, light) et éviter la duplication de code
    @staticmethod
    def decode_output(string: str) -> int:
        """Return the bit position in the OUT_STATE or MEM_STATE for an output string like "Q1" or "M1"."""
        if string.startswith(("Q", "M")):
            return int(string[1:]) - 1
        elif string.startswith("Y"):
            return 8 + int(string[1:]) - 1
        else:
            raise ValueError(f"Output string '{string}' is invalid.")

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
        return f"ismart_cover_{self._device_id}_{self._up_coil}"

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

    def __init__(self, *args, **kwargs):
        """Initialize the garage door entity."""
        super().__init__(*args, **kwargs)
        #self._is_opening = False
        #self._is_closing = False
        self._last_direction = None

    async def async_open_cover(self, **kwargs):
        """Open the garage door."""
        if self.is_opened:
            return
        if (await self._modbus_interface.write_coil(self._up_coil) == True):
            self._last_direction = "up"
        await self.coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs):
        """Close the garage door."""
        if self.is_closed:
            return
        if (await self._modbus_interface.write_coil(self._down_coil) == True):
            self._last_direction = "down"
        await self.coordinator.async_request_refresh()

    @property
    def is_opening(self) -> bool:
        state = self.coordinator.get_bit(self._device_id, self._opening_flag) and self._last_direction == "up"
        return bool(state)

    @property
    def is_closing(self) -> bool:
        state = self.coordinator.get_bit(self._device_id, self._closing_flag) and self._last_direction == "down"
        return bool(state)

    # A vérifier !!!!!!!
    @property
    def device_class(self) -> str:
        """Return the class of this device."""
        return "garage"