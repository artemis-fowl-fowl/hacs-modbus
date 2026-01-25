"""Shutter platform for iSMART Modbus."""
import logging
from homeassistant.components.cover import CoverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.cover import CoverEntity, CoverState

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
                up_input=device_info["up_input"],
                down_input=device_info["down_input"],
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

    def __init__(self, coordinator, name, device_id, up_input, down_input, up_bit, down_bit, open_bit, closed_bit, device_class, modbus_interface):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._name = name
        self._device_id = device_id
        self._up_coil = self.decode_input(up_input)     # Trouve l'addresse du coil correspondant à l'entrée
        self._down_coil = self.decode_input(down_input)     # Trouve l'addresse du coil correspondant à l'entrée
        self._up_bit = up_bit
        self._down_bit = down_bit
        self._open_bit = open_bit
        self._closed_bit = closed_bit
        self._device_class = device_class
        self._modbus = modbus_interface

    @staticmethod
    def decode_input(string):
        """Return the Ismart coil address of an input string like "I1" or "X1" """
        if string.startswith("I"):
            return 0x550 + int(string[1:]) - 1
        elif string.startswith("X"):
            return 0x560 + int(string[1:]) - 1
        else:
            raise ValueError(f"Input string '{string}' is invalid.")

    @staticmethod
    def decode_output(string):
        """Returns the bit position in the OUT_STATE value for output string like "Q1" or "Y1" """
        if string.startswith("Q"):
            return int(string[1:]) - 1
        elif string.startswith("Y"):
            return 8 + int(string[1:]) - 1
        else:
            raise ValueError(f"output string '{string}' is invalid.")

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"ismart_{self._device_id}_{self._up_coil}"

    @property
    def assumed_state(self) -> bool:
        return False

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
    def is_closed(self):
        """Return true if the shutter is up."""
        # Récupérer l'état depuis le coordinateur
        state = self.coordinator.get_bit(self._device_id, self._closed_bit)
        return state if state is not None else False

    # is_open n'est pas une propriété native des entity cover.
    # J'ai ajouté cette propriété pour pouvoir détecté l'état unknow
    @property
    def is_open(self):
        """Return true if the shutter is up."""
        # Récupérer l'état depuis le coordinateur
        state = self.coordinator.get_bit(self._device_id, self._open_bit)
        return state if state is not None else False
    

    # Par défaut le front end se charge de calculer state en fonction de is_opening, is_closing et is_close
    # Mais il impose l'état OPEN par défaut.
    # On gère donc ici la propriété "state" pour pouvoir imposer un état inconnu avec state = None quand la position est inconnue
    # Cela permet entre autre de conserver la commande down qui se retrouve grisée si on est en état "OPEN"
    @property
    def state(self):
        """Return the state of the cover."""
        if self.is_opening:
            state = CoverState.OPENING
        elif self.is_closing:
            state = CoverState.CLOSING
        elif self.is_closed:
            state = CoverState.CLOSED
        elif self.is_open:
            state = CoverState.OPEN
        else:
            state = None
        _LOGGER.warning(f"volet {self.name} state is {str(state)}")
        return state
        #return CoverState.CLOSING
 

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.is_device_available(self._device_id)

    @property
    def icon(self) -> str | None:
        """Return the icon."""
        #if self._device_class == "cover":
        #if not self.available:
        #    return "mdi:window-shutter-alert"
        if self.is_opening:
            return "mdi:window-shutter-cog"
        if self.is_closing:
            return "mdi:window-shutter-cog"
        if self.is_closed:
            return "mdi:window-shutter"
        if self.is_open:
            return "mdi:window-shutter-open"
        return "mdi:window-shutter-alert"


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

    async def async_stop_cover(self, **kwargs):
        """Stop the cover using the up_coil or the down_coil."""
        try:
            #await self.coordinator.async_request_refresh()
            if self.is_opening:
                coil = self._up_coil
            elif self.is_closing:
                coil = self._down_coil
            else:   #Si on est pas en mouvement il n'y a pas lieu de faire un stop
                return
            if await self.hass.async_add_executor_job(self._modbus.writecoil_device, self._device_id, coil, 1) == 0:
                _LOGGER.info("Cover %s stopped", self._name)
                await self.coordinator.async_request_refresh()  # Rafraîchir immédiatement l'état
            else:
                _LOGGER.error("Failed to stop cover %s", self._name)
        except Exception as e:
            _LOGGER.error("Error stopping %s: %s", self._name, e)