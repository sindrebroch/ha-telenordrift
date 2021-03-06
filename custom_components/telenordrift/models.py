"""Models for TelenorDrift."""

from typing import Any, Dict, List

import attr

from .const import LOGGER

@attr.s(auto_attribs=True)
class AffectedPlatform:
    """Class representing AffectedPlatform."""

    affectedPlatforms: str
    description: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "AffectedPlatform":
        """Transform data to dict."""

        LOGGER.debug("AffectedPlatform=%s", data)

        return AffectedPlatform(
            affectedPlatforms=data["affectedPlatforms"],
            description=data["description"],
        )


@attr.s(auto_attribs=True)
class TelenorDriftResponse:
    """Class representing TelenorDrift."""

    platforms: List[AffectedPlatform]

    @staticmethod
    def from_dict(data: List[Dict[str, Any]]) -> "TelenorDriftResponse":
        """Transform data to dict."""

        LOGGER.debug("TelenorDriftResponse=%s", data)

        platforms: List[AffectedPlatform] = []
        for platform in data:
            platforms.append(AffectedPlatform.from_dict(platform))

        return TelenorDriftResponse(platforms=platforms)
