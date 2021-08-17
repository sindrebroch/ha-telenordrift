"""The TelenorDrift integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from async_timeout import timeout
from voluptuous.error import Error

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_AREA, DOMAIN as TELENORDRIFT_DOMAIN
from .models import TelenorDriftResponse
from .telenordrift import TelenorDrift

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the TelenorDrift integration."""

    _LOGGER.warning("Async setup")

    hass.data[TELENORDRIFT_DOMAIN] = {}

    if TELENORDRIFT_DOMAIN in config:
        for conf in config[TELENORDRIFT_DOMAIN]:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    TELENORDRIFT_DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
                )
            )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TelenorDrift from a config entry."""

    _LOGGER.warning("Async setup entry")

    websession = async_get_clientsession(hass)
    area = entry.data[CONF_AREA]

    coordinator = TelenorDriftDataUpdateCoordinator(hass, websession, area)

    await coordinator.async_config_entry_first_refresh()

    entry.async_on_unload(entry.add_update_listener(update_listener))

    hass.data.setdefault(TELENORDRIFT_DOMAIN, {})[entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[TELENORDRIFT_DOMAIN].pop(entry.entry_id)

    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""

    await hass.config_entries.async_reload(entry.entry_id)


class TelenorDriftDataUpdateCoordinator(DataUpdateCoordinator[TelenorDriftResponse]):
    """Class to manage fetching TelenorDrift data API."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
        area: str,
    ) -> None:
        """Initialize."""

        update_interval = timedelta(minutes=60)

        self.area: str = area
        self.telenordrift: TelenorDrift = TelenorDrift(area=area, session=session)

        super().__init__(
            hass,
            _LOGGER,
            name=TELENORDRIFT_DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> TelenorDriftResponse:
        """Update data via library."""

        try:
            async with timeout(10):
                telenordrift = await self.telenordrift.fetch()

        except (Error, ClientConnectorError) as error:
            _LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error

        return telenordrift