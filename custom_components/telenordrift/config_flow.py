"""Config flow for Pollenvarsel integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from .pollenvarsel import Pollenvarsel
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import AREA_PATH, CONF_AREA, DOMAIN as POLLENVARSEL_DOMAIN
from .models import Area

_LOGGER = logging.getLogger(__name__)

AREA_KEYS: list[str] = [area.name for area in AREA_PATH.keys()]
SCHEMA = vol.Schema({vol.Required(CONF_AREA): vol.In(sorted(AREA_KEYS))})


class PollenvarselFlowHandler(config_entries.ConfigFlow, domain=POLLENVARSEL_DOMAIN):
    """Config flow for Pollenvarsel."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:

            optional_area: str | None = user_input.get(CONF_AREA)

            if optional_area is not None:

                area: Area = Area.from_str(optional_area)

                if await self._async_existing_devices(area.name):
                    return self.async_abort(reason="already_configured")

                session = async_get_clientsession(self.hass)
                pollenvarsel = Pollenvarsel(area=area, session=session)

                errors: dict[str, Any] = {}

                try:
                    await pollenvarsel.fetch()
                except aiohttp.ClientError as error:
                    errors["base"] = "cannot_connect"
                    _LOGGER.warning("error=%s. errors=%s", error, errors)

                if errors:
                    return self.async_show_form(
                        step_id="user", data_schema=SCHEMA, errors=errors
                    )

                unique_id: str = pollenvarsel.area.name
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

        _LOGGER.warning("current_entries=%s", self._async_current_entries())
        existing_devices = [
            f"{entry.data.get(CONF_AREA)}" for entry in self._async_current_entries()
        ]
        _LOGGER.warning("existing_devices=%s", existing_devices)

        return area in existing_devices
