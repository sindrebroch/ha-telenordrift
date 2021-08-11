"""Config flow for TelenorDrift integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_AREA, DOMAIN as TELENORDRIFT_DOMAIN
from .telenordrift import TelenorDrift

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_AREA): str,
    }
)

_LOGGER = logging.getLogger(__name__)


class TelenorDriftFlowHandler(config_entries.ConfigFlow, domain=TELENORDRIFT_DOMAIN):
    """Config flow for TelenorDrift."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:

            area = user_input[CONF_AREA]

            if await self._async_existing_devices(area):
                return self.async_abort(reason="already_configured")

            session = async_get_clientsession(self.hass)
            telenordrift = TelenorDrift(area=area, session=session)

            errors: dict[str, Any] = {}

            try:
                await telenordrift.fetch()  # TODO https://www.telenor.no/system/address-search/?q=address
            except aiohttp.ClientError as error:
                errors["base"] = "cannot_connect"
                _LOGGER.warning("error=%s. errors=%s", error, errors)

            if errors:
                return self.async_show_form(
                    step_id="user", data_schema=SCHEMA, errors=errors
                )

            unique_id: str = area
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=unique_id.title(),
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors={},
        )

    async def _async_existing_devices(self, area: str) -> bool:
        """Find existing devices."""

        existing_devices = [
            f"{entry.data.get(CONF_AREA)}" for entry in self._async_current_entries()
        ]

        return area in existing_devices
