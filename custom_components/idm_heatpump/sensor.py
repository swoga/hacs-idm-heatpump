"""Sensor platform for idm_heatpump."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import IdmHeatpumpDataUpdateCoordinator
from .sensor_addresses import IdmSensorAddress
from .const import DOMAIN
from .entity import IdmHeatpumpEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    coordinator: IdmHeatpumpDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            IdmHeatpumpSensor(coordinator, entry, address)
            for address in coordinator.heatpump.sensors
            if isinstance(address, IdmSensorAddress)
        ],
    )


class IdmHeatpumpSensor(IdmHeatpumpEntity, SensorEntity):
    """IDM heatpump sensor class."""

    def __init__(
        self,
        coordinator: IdmHeatpumpDataUpdateCoordinator,
        config_entry: ConfigEntry,
        sensor_address: IdmSensorAddress
    ):
        """Create sensor."""
        super().__init__(coordinator, config_entry)
        self.sensor_address = sensor_address
        self.entity_description = self.sensor_address.entity_description(
            config_entry
        )

    @property
    def sensor_id(self):
        """Return sensor id."""
        return self.sensor_address.name

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.sensor_address.name)
