

import aiohttp
import pytest
import socket

from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.telenordrift.api import TelenorDriftApiClient
from custom_components.telenordrift.const import LOGGER

@pytest.mark.asyncio
async def test_api_ping(hass):

    async with aiohttp.ClientSession() as session:
        api = TelenorDriftApiClient(
            area = '168443300',
            postCode = '0010',
            session = session
        )


        LOGGER.info('TEST')

        res = await api.fetch()

        LOGGER.info(res)
