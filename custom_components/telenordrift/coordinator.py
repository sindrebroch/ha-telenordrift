"""Telenordrift data coordinator"""

from datetime import timedelta

from aiohttp.client import ClientSession
from aiohttp.client_exceptions import ClientConnectorError
from voluptuous.error import Error

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import TelenorDriftApiClient
from .const import DOMAIN as TELENORDRIFT_DOMAIN, LOGGER
from .models import TelenorDriftResponse

class TelenorDriftDataUpdateCoordinator(DataUpdateCoordinator[TelenorDriftResponse]):
    """Class to manage fetching TelenorDrift data API."""

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
        area: str,
        postCode: str,
    ) -> None:
        """Initialize."""

        update_interval = timedelta(minutes=60)

        self.area: str = area
        self.postCode: str = postCode
        self.api = TelenorDriftApiClient(area=area, postCode=postCode, session=session)

        self._attr_device_info = DeviceInfo(
            name="TelenorDrift",
            manufacturer="TelenorDrift",
            model="TelenorDrift",
            identifiers={(TELENORDRIFT_DOMAIN, "telenordrift")},
            configuration_url="https://www.telenor.no/driftsmeldinger/",
        )

        super().__init__(
            hass,
            LOGGER,
            name=TELENORDRIFT_DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> TelenorDriftResponse:
        """Update data via library."""

        try:
            return await self.api.fetch()
        except (Error, ClientConnectorError) as error:
            LOGGER.error("Update error %s", error)
            raise UpdateFailed(error) from error
