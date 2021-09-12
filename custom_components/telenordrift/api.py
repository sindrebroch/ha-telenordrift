"""TelenorDrift library."""

import json
from typing import Any, Optional

import socket
import asyncio
import aiohttp
import async_timeout
from voluptuous.error import Error

from homeassistant.const import HTTP_OK, HTTP_UNAUTHORIZED

from .const import LOGGER
from .models import TelenorDriftResponse


class ApiClientException(Exception):
    """Api Client Exception."""


class TelenorDriftApiClient:
    """Main class for handling connection with."""

    def __init__(
        self,
        area: str,
        session: Optional[aiohttp.client.ClientSession] = None,
    ) -> None:
        """Initialize connection with TelenorDrift."""

        self._session = session
        self.area: str = area

    async def fetch(self) -> TelenorDriftResponse:
        """Fetch data from TelenorDrift."""

        if self._session is None:
            raise RuntimeError("Session required")

        URL = f"https://www.telenor.no/system/service-messages/status/{self.area}"
        LOGGER.debug("Fetching telenordrift URL=%s", URL)

        async with self._session.get(url=URL) as resp:
            if resp.status == HTTP_UNAUTHORIZED:
                raise Error(f"Unauthorized. {resp.status}")
            if resp.status != HTTP_OK:
                error_text = json.loads(await resp.text())
                raise Error(f"Not OK {resp.status} {error_text}")

            data = await resp.json()

        LOGGER.debug("Response %s", data)
        return TelenorDriftResponse.from_dict(data)

    async def api_wrapper(
        self,
        method: str,
        url: str,
    ) -> dict[str, Any] or None:
        """Wrap request."""

        LOGGER.debug("%s-request to url=%s.", method, url)

        try:
            async with async_timeout.timeout(10, loop=asyncio.get_event_loop()):
                response = await self._session.request(method=method, url=url)
                return await response.json()
        except asyncio.TimeoutError as exception:
            raise ApiClientException(
                f"Timeout error fetching information from {url}"
            ) from exception
        except (KeyError, TypeError) as exception:
            raise ApiClientException(
                f"Error parsing information from {url} - {exception}"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ApiClientException(
                f"Error fetching information from {url} - {exception}"
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise ApiClientException(exception) from exception