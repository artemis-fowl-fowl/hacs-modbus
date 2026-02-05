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

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

EM111_UNITS = [10, 11, 12]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up EM111 sensors."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    coordinator = entry_data["coordinator"]

    entities: list[SensorEntity] = []

    for unit_id in EM111_UNITS:
        entities.append(
            ISmartEM111PowerSensor(coordinator, unit_id)
        )
        entities.append(
            ISmartEM111EnergySensor(coordinator, unit_id)
        )

    async_add_entities(entities)


# -------------------------------------------------------------------
# Base class
# -------------------------------------------------------------------

class ISmartEM111BaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for EM111 sensors."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, unit_id: int):
        super().__init__(coordinator)
        self._unit_id = unit_id

    @property
    def available(self) -> bool:
        """Sensor is available if EM111 data exists."""
        data = self.coordinator.data.get("em111", {})
        return self._unit_id in data and data[self._unit_id] is not None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"em111_{self._unit_id}")},
            "name": f"EM111 {self._unit_id}",
            "manufacturer": "Eastron",
            "model": "EM111",
        }


# -------------------------------------------------------------------
# Power sensor
# -------------------------------------------------------------------

class ISmartEM111PowerSensor(ISmartEM111BaseSensor):
    """Instantaneous power sensor."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "W"

    def __init__(self, coordinator, unit_id: int):
        super().__init__(coordinator, unit_id)
        self._attr_unique_id = f"ismart_em111_{unit_id}_power"
        self._attr_name = "Power"

    @property
    def native_value(self):
        data = self.coordinator.data.get("em111", {})
        em = data.get(self._unit_id)
        if not em:
            return None
        return em.get("power_w")


# -------------------------------------------------------------------
# Energy sensor
# -------------------------------------------------------------------

class ISmartEM111EnergySensor(ISmartEM111BaseSensor):
    """Total energy sensor."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = "kWh"

    def __init__(self, coordinator, unit_id: int):
        super().__init__(coordinator, unit_id)
        self._attr_unique_id = f"ismart_em111_{unit_id}_energy"
        self._attr_name = "Energy"

    @property
    def native_value(self):
        data = self.coordinator.data.get("em111", {})
        em = data.get(self._unit_id)
        if not em:
            return None
        return em.get("energy_kwh")
