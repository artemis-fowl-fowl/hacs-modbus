"""Sensor platform for iSMART Modbus (EM111 energy meters)."""

import logging
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, EM111_DEVICES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EM111 sensors."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    coordinator = entry_data["coordinator"]

    entities: list[SensorEntity] = []

    for dev in EM111_DEVICES:
        name = dev["name"]
        device_id = dev["device_id"]

        entities.append(EM111VoltageSensor(coordinator, name, device_id))
        entities.append(EM111CurrentSensor(coordinator, name, device_id))
        entities.append(EM111PowerSensor(coordinator, name, device_id))
        entities.append(EM111PowerDmdSensor(coordinator, name, device_id))
        entities.append(EM111PowerDmdPeakSensor(coordinator, name, device_id))
        entities.append(EM111FrequencySensor(coordinator, name, device_id))
        entities.append(EM111EnergySensor(coordinator, name, device_id))

    async_add_entities(entities)


class EM111BaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for EM111 sensors."""

    def __init__(self, coordinator, name: str, device_id: int):
        super().__init__(coordinator)
        self._name = name
        self._device_id = device_id

    @property
    def name(self):
        return self._attr_name

    @property
    def available(self) -> bool:
        """Sensor is available if EM111 data exists."""
        data = self.coordinator.data.get("em111", {})
        return self._name in data and data[self._name] is not None


class EM111VoltageSensor(EM111BaseSensor):
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "V"

    def __init__(self, coordinator, name: str, device_id: int):
        super().__init__(coordinator, name, device_id)
        self._attr_unique_id = f"em111_{name}_voltage"
        self._attr_name = f"{name} Voltage"

    @property
    def native_value(self):
        em = self.coordinator.data.get("em111", {}).get(self._name)
        return em.get("voltage") if em else None


class EM111CurrentSensor(EM111BaseSensor):
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "A"

    def __init__(self, coordinator, name: str, device_id: int):
        super().__init__(coordinator, name, device_id)
        self._attr_unique_id = f"em111_{name}_current"
        self._attr_name = f"{name} Current"

    @property
    def native_value(self):
        em = self.coordinator.data.get("em111", {}).get(self._name)
        return em.get("current") if em else None


class EM111PowerSensor(EM111BaseSensor):
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "W"

    def __init__(self, coordinator, name: str, device_id: int):
        super().__init__(coordinator, name, device_id)
        self._attr_unique_id = f"em111_{name}_power"
        self._attr_name = f"{name} Power"

    @property
    def native_value(self):
        em = self.coordinator.data.get("em111", {}).get(self._name)
        return em.get("power") if em else None


class EM111PowerDmdSensor(EM111BaseSensor):
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "W"

    def __init__(self, coordinator, name: str, device_id: int):
        super().__init__(coordinator, name, device_id)
        self._attr_unique_id = f"em111_{name}_power_dmd"
        self._attr_name = f"{name} Power Demand"

    @property
    def native_value(self):
        em = self.coordinator.data.get("em111", {}).get(self._name)
        return em.get("power_dmd") if em else None


class EM111PowerDmdPeakSensor(EM111BaseSensor):
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "W"

    def __init__(self, coordinator, name: str, device_id: int):
        super().__init__(coordinator, name, device_id)
        self._attr_unique_id = f"em111_{name}_power_dmd_peak"
        self._attr_name = f"{name} Power Demand Peak"

    @property
    def native_value(self):
        em = self.coordinator.data.get("em111", {}).get(self._name)
        return em.get("power_dmd_peak") if em else None


class EM111FrequencySensor(EM111BaseSensor):
    _attr_device_class = SensorDeviceClass.FREQUENCY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "Hz"

    def __init__(self, coordinator, name: str, device_id: int):
        super().__init__(coordinator, name, device_id)
        self._attr_unique_id = f"em111_{name}_frequency"
        self._attr_name = f"{name} Frequency"

    @property
    def native_value(self):
        em = self.coordinator.data.get("em111", {}).get(self._name)
        return em.get("frequency") if em else None


class EM111EnergySensor(EM111BaseSensor):
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = "kWh"

    def __init__(self, coordinator, name: str, device_id: int):
        super().__init__(coordinator, name, device_id)
        self._attr_unique_id = f"em111_{name}_energy"
        self._attr_name = f"{name} Energy"

    @property
    def native_value(self):
        em = self.coordinator.data.get("em111", {}).get(self._name)
        return em.get("energy") if em else None
