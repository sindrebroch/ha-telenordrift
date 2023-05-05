"""The TelenorDrift integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_AREA, DOMAIN as TELENORDRIFT_DOMAIN, PLATFORMS
from .coordinator import TelenorDriftDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TelenorDrift from a config entry."""

    hass.data.setdefault(TELENORDRIFT_DOMAIN, {})

    coordinator = TelenorDriftDataUpdateCoordinator(
        hass, 
        async_get_clientsession(hass), 
        entry.data[CONF_AREA],
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[TELENORDRIFT_DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[TELENORDRIFT_DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
