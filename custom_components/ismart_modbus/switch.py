"""Switch platform for iSMART Modbus."""
import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, SWITCH_DEVICES

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
    for device_info in SWITCH_DEVICES:
        entities.append(
            ISmartModbusSwitch(
                coordinator=coordinator,
                name=device_info["name"],
                device_id=device_info["device_id"],
                input=device_info["input"],
                bit_position=device_info["bit_position"],
                device_class=device_info["device_class"],
                modbus_interface=modbus_interface,
            )
        )

    async_add_entities(entities)


class ISmartModbusSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of an iSMART Modbus Switch."""

    def __init__(self, coordinator, name, device_id, input, output, device_class, modbus_interface):
        """Initialize the switch."""
        super().__init__(coordinator)
        self._name = name
        self._device_id = device_id
        self._device_class = device_class
        self._modbus = modbus_interface
        self._coil = self.decode_input(input)           # Trouve l'addresse du coil correspondant à l'entrée
        self._bit_position =self.decode_output(output)  # Trouve la position du bit dans OUT_STATE
    @staticmethod
    def decode_input(string):
        """Return the Ismart coil address of an input string like "I1" or "X1" """
        if string.startswith("I"):
            return 0x0550 + int(string[1:]) - 1
        elif string.startswith("X"):
            return 0x0560 + int(string[1:]) - 1
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
        return f"ismart_{self._device_id}_{self._coil}"

    @property
    def is_on(self):
        """Return true if switch is on."""
        # Récupérer l'état depuis le coordinateur
        state = self.coordinator.get_bit(device_id = self._device_id, bit_position = self._bit_position)
        return state if state is not None else False

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.is_device_available(self._device_id)
 
    @property
    def icon(self):
        """Return the icon."""
        #if self._device_class == "cover":
        #if not self.available:
        #    return "mdi:lightbulb-alert"
        if self.is_on:
            return "mdi:lightbulb-on"
        return "mdi:lightbulb-off"


    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        try:
            result = await self.hass.async_add_executor_job(
                self._modbus.writecoil_device,
                self._device_id,
                self._coil,
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

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        try:
            result = await self.hass.async_add_executor_job(
                self._modbus.writecoil_device,
                self._device_id,
                self._coil,
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
