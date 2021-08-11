"""Sensor file for TelenorDrift."""

import logging
from typing import Final, List, Optional, Tuple, cast

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN as TELENORDRIFT_DOMAIN
from .models import TelenorDriftResponse

SENSORS: Final[Tuple[SensorEntityDescription, ...]] = (
    SensorEntityDescription(
        key="tv",
        name="TV",
        icon="mdi:television",
    ),
    SensorEntityDescription(
        key="internett",
        name="Internett",
        icon="mdi:router-wireless",
    ),
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add TelenorDrift entities from a config_entry."""

    coordinator: DataUpdateCoordinator = hass.data[TELENORDRIFT_DOMAIN][entry.entry_id]

    sensors: List[TelenorDriftSensor] = []

    for sensor_description in SENSORS:
        sensors.append(
            TelenorDriftSensor(coordinator, sensor_description),
        )

    async_add_entities(sensors)


class TelenorDriftSensor(CoordinatorEntity, SensorEntity):
    """Define a TelenorDrift entity."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)

        self.entity_description = description

        self.sensor_data: List[str] = _get_sensor_data(
            coordinator.data, description.key
        )

        self._attr_name = f"{description.name}"
        self._attr_unique_id = f"{description.key}"

    @property
    def state(self) -> StateType:
        """Return the state."""

        return cast(StateType, len(self.sensor_data))

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        return {"issues": self.sensor_data}

    @property
    def device_info(self) -> Optional[DeviceInfo]:
        """Return the device info."""

        return {
            "identifiers": {(TELENORDRIFT_DOMAIN, "telenordrift")},
            "name": "TelenorDrift",
            "model": "TelenorDrift",
            "manufacturer": "TelenorDrift",
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = _get_sensor_data(
            self.coordinator.data, self.entity_description.key
        )
        self.async_write_ha_state()


def _get_sensor_data(sensors: TelenorDriftResponse, sensor_name: str) -> List[str]:
    """Get sensor data."""

    _LOGGER.warning("Finding state for %s", sensor_name)
    _LOGGER.warning("%s", sensors)

    issues: List[str] = []

    for platform in sensors.platforms:
        if sensor_name in platform.affectedPlatforms:
            issues.append(platform.description)

        for affected in platform.affectedPlatforms:
            if affected != "tv" and affected != "internett":
                _LOGGER.warning("Ukjent platform for telenordrift %s", affected)

    return issues
