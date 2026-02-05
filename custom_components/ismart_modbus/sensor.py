from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class EM111PowerSensor(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = "W"

    def __init__(self, coordinator, unit_id: int):
        super().__init__(coordinator)
        self._unit_id = unit_id
        self._attr_name = f"EM111 Puissance {unit_id}"
        self._attr_unique_id = f"em111_power_{unit_id}"

    @property
    def native_value(self):
        return self.coordinator.data[self._unit_id]["power_w"]


class EM111EnergySensor(CoordinatorEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = "kWh"

    def __init__(self, coordinator, unit_id: int):
        super().__init__(coordinator)
        self._unit_id = unit_id
        self._attr_name = f"EM111 Énergie {unit_id}"
        self._attr_unique_id = f"em111_energy_{unit_id}"

    @property
    def native_value(self):
        return self.coordinator.data[self._unit_id]["energy_kwh"]
