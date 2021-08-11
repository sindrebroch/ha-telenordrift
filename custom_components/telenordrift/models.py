"""Models for TelenorDrift."""

import json
import logging
from typing import Any, Dict, List

import attr

_LOGGER = logging.getLogger(__name__)


@attr.s(auto_attribs=True, frozen=True)
class AffectedPlatform:
    """Class representing AffectedPlatform."""

    affectedPlatforms: str
    description: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "AffectedPlatform":
        """Transform data to dict."""

        _LOGGER.warning("AffectedPlatform from_dict %s", data)

        return AffectedPlatform(
            affectedPlatforms=data["affectedPlatforms"],
            description=data["description"],
        )


@attr.s(auto_attribs=True, frozen=True)
class TelenorDriftResponse:
    """Class representing TelenorDrift."""

    platforms: List[AffectedPlatform]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "TelenorDriftResponse":
        """Transform data to dict."""

        _LOGGER.warning("TelenorDriftResponse from_dict %s", data)

        platforms: List[AffectedPlatform] = []
        for platform in data:
            platforms.append(AffectedPlatform.from_dict(json.loads(platform)))

        return TelenorDriftResponse(platforms=platforms)
