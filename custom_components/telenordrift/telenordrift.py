"""TelenorDrift library."""

import json
import logging
from typing import Optional

import aiohttp
from voluptuous.error import Error

from homeassistant.const import HTTP_OK, HTTP_UNAUTHORIZED

from .models import TelenorDriftResponse

_LOGGER = logging.getLogger(__name__)


class TelenorDrift:
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
        _LOGGER.warning("Fetching telenordrift URL=%s", URL)

        async with self._session.get(url=URL) as resp:
            if resp.status == HTTP_UNAUTHORIZED:
                raise Error(f"Unauthorized. {resp.status}")
            if resp.status != HTTP_OK:
                error_text = json.loads(await resp.text())
                raise Error(f"Not OK {resp.status} {error_text}")

            data = await resp.json()

        _LOGGER.warning("Response %s", data)
        return TelenorDriftResponse.from_dict(data)