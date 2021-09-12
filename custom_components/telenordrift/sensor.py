"""Sensor file for TelenorDrift."""

from typing import List, cast

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN as TELENORDRIFT_DOMAIN, LOGGER
from .coordinator import TelenorDriftDataUpdateCoordinator
from .models import TelenorDriftResponse

CONST_TV = "TV"
CONST_INTERNETT = "INTERNETT"
CONST_MOBILE = "MOBILE"

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key=CONST_TV,
        name="TV",
        icon="mdi:television",
        native_unit_of_measurement="feil",
    ),
    SensorEntityDescription(
        key=CONST_INTERNETT,
        name="Internett",
        icon="mdi:router-wireless",
        native_unit_of_measurement="feil",
    ),
    SensorEntityDescription(
        key=CONST_MOBILE,
        name="Mobile",
        icon="mdi:cellphone",
        native_unit_of_measurement="feil",
    ),
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add TelenorDrift entities from a config_entry."""

    coordinator: TelenorDriftDataUpdateCoordinator = hass.data[TELENORDRIFT_DOMAIN][entry.entry_id]

    for sensor_description in SENSORS:
        async_add_entities(TelenorDriftSensor(coordinator, sensor_description))


class TelenorDriftSensor(CoordinatorEntity, SensorEntity):
    """Define a TelenorDrift entity."""

    coordinator: TelenorDriftDataUpdateCoordinator

    def __init__(
        self,
        coordinator: TelenorDriftDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)

        self.coordinator = coordinator
        self.entity_description = description
        self.sensor_data: List[str] = _get_sensor_data(
            coordinator.data, description.key
        )

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info
        self._attr_extra_state_attributes = {"issues": self.sensor_data}

    @property
    def native_value(self) -> StateType:
        """Return the state."""

        return cast(StateType, len(self.sensor_data))

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = _get_sensor_data(
            self.coordinator.data, self.entity_description.key
        )
        self.async_write_ha_state()


def _get_sensor_data(sensors: TelenorDriftResponse, sensor_name: str) -> List[str]:
    """Get sensor data."""

    LOGGER.debug("Finding state for %s", sensor_name)
    LOGGER.debug("%s", sensors)

    issues: List[str] = []

    for platform in sensors.platforms:
        if sensor_name in platform.affectedPlatforms:
            issues.append(
                "Ingen beskrivelse" if platform.description is None else platform.description
            )

        for affected in platform.affectedPlatforms:
            if affected not in (CONST_TV, CONST_INTERNETT, CONST_MOBILE):
                LOGGER.warning("Ukjent platform for telenordrift %s", affected)

    return issues
