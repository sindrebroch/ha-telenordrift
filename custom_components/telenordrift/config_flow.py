"""Config flow for TelenorDrift integration."""

from __future__ import annotations

from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import TelenorDriftApiClient
from .const import CONF_AREA, CONF_POSTCODE, DOMAIN as TELENORDRIFT_DOMAIN, LOGGER

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_AREA): str,
        vol.Required(CONF_POSTCODE): str
    }
)

class TelenorDriftFlowHandler(config_entries.ConfigFlow, domain=TELENORDRIFT_DOMAIN):
    """Config flow for TelenorDrift."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:

            area = user_input[CONF_AREA]
            postCode = user_input[CONF_POSTCODE]

            await self.async_set_unique_id(area)
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            api = TelenorDriftApiClient(area=area, postCode=postCode, session=session)

            errors: dict[str, Any] = {}

            try:
                await api.fetch()  # TODO https://www.telenor.no/system/address-search/?q=address
            except aiohttp.ClientError as error:
                errors["base"] = "cannot_connect"
                LOGGER.warning("error=%s. errors=%s", error, errors)

            if errors:
                return self.async_show_form(
                    step_id="user", data_schema=SCHEMA, errors=errors
                )

            return self.async_create_entry(
                title=area.title(),
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors={},
        )
