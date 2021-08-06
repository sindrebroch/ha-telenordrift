"""Sensor file for pollenvarsel."""

from enum import IntEnum
import logging
from typing import Final, List, Optional, Tuple, cast

from .const import (
    CONF_AREA,
    DOMAIN as POLLENVARSEL_DOMAIN,
)
from .models import (
    Allergen,
    Area,
    PollenForecast,
    PollenvarselResponse,
)
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

_LOGGER = logging.getLogger(__name__)

ENTITY_SALIX: Final[str] = "salix"
ENTITY_BJORK: Final[str] = "bjørk"
ENTITY_OR: Final[str] = "or"
ENTITY_HASSEL: Final[str] = "hassel"
ENTITY_GRESS: Final[str] = "gress"
ENTITY_BUROT: Final[str] = "burot"

SENSORS: Final[Tuple[SensorEntityDescription, ...]] = (
    SensorEntityDescription(
        key=ENTITY_SALIX,
        name="Salix",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=ENTITY_BJORK,
        name="Bjørk",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=ENTITY_OR,
        name="Or",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=ENTITY_HASSEL,
        name="Hassel",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=ENTITY_GRESS,
        name="Gress",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key=ENTITY_BUROT,
        name="Burot",
        icon="mdi:tree",
    ),
)


class Day(IntEnum):
    """Enum representing type of Day."""

    TODAY = 0
    TOMORROW = 1


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add Pollenvarsel entities from a config_entry."""

    coordinator: DataUpdateCoordinator = hass.data[POLLENVARSEL_DOMAIN][entry.entry_id]

    area: Optional[Area] = Area.from_str(entry.data[CONF_AREA])  #

    sensors: List[PollenvarselSensor] = []

    if area is not None:
        for sensor_description in SENSORS:
            sensors.append(
                PollenvarselSensor(
                    area,
                    coordinator,
                    sensor_description,
                    Day.TODAY,
                ),
            )
            sensors.append(
                PollenvarselSensor(
                    area,
                    coordinator,
                    sensor_description,
                    Day.TOMORROW,
                ),
            )

    async_add_entities(sensors)


class PollenvarselSensor(CoordinatorEntity, SensorEntity):
    """Define a Pollenvarsel entity."""

    def __init__(
        self,
        area: Area,
        coordinator: DataUpdateCoordinator,
        description: SensorEntityDescription,
        day: Day,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)

        self.entity_description = description

        self.day: Day = Day(day)
        self.area: Area = Area(area)
        self.sensor_data: str = _get_sensor_data(coordinator.data, day, description.key)

        if day == Day.TODAY:
            self._attr_unique_id = f"{self.area.name}_{description.key}"
            self._attr_name = f"{self.area.name.title()} {description.key}"
        else:
            day_string: str = "imorgen" if day == Day.TOMORROW else ""
            self._attr_name = f"{self.area.name.title()} {description.key} {day_string}"
            self._attr_unique_id = f"{self.area.name}_{description.key}_{day_string}"

    @property
    def state(self) -> StateType:
        """Return the state."""

        return cast(StateType, self.sensor_data)

    @property
    def device_info(self) -> Optional[DeviceInfo]:
        """Return the device info."""

        return {
            "identifiers": {(POLLENVARSEL_DOMAIN, self.area.name)},
            "name": f"Pollenvarsel {self.area.name.title()}",
            "model": "Pollenvarsel",
            "manufacturer": f"{self.area.name.title()}",
        }

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""

        self.sensor_data = _get_sensor_data(
            self.coordinator.data, self.day, self.entity_description.key
        )
        self.async_write_ha_state()


def _get_sensor_data(sensors: PollenvarselResponse, day: Day, sensor_name: str) -> str:
    """Get sensor data."""

    forecasts: List[PollenForecast] = sensors.forecast
    current_day_forecast: PollenForecast = forecasts.__getitem__(day.value)
    allergens: List[Allergen] = current_day_forecast.allergens

    for allergen in allergens:
        if allergen.name.lower() == sensor_name.lower():
            return allergen.level_description

    _LOGGER.warning("Could not find state for sensor.%s", sensor_name)

    return ""
