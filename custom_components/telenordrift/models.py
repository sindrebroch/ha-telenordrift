"""Models for Pollenvarsel."""

from enum import Enum
import logging
from typing import Any, Dict, List

import attr

_LOGGER = logging.getLogger(__name__)


class Area(Enum):
    """Enum representing area."""

    TROMS = "troms"
    FINNMARK = "finnmark"
    NORDLAND = "nordland"
    ROGALAND = "rogaland"
    SØRLANDET = "sørlandet"
    TRØNDELAG = "trøndelag"
    HORDALAND = "hordaland"
    INDRE_ØSTLAND = "indre_østland"
    MØRE_OG_ROMSDAL = "møre_og_romsdal"
    SOGN_OG_FJORDANE = "sogn_og_fjordane"
    ØSTLANDET_MED_OSLO = "østlandet_med_oslo"
    SENTRALE_FJELLSTRØK_I_SØR_NORGE = "sentrale_fjellstrøk_i_sør_norge"

    @staticmethod
    def from_str(label: str) -> "Area":
        """Find enum from string."""

        for area in Area:
            if label.lower() == area.name.lower():
                return area

        raise NotImplementedError


@attr.s(auto_attribs=True, frozen=True)
class PollenStation:
    """Class representing PollenStation."""

    name: str
    country_code: str
    distance_in_km: float

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PollenStation":
        """Transform data to dict."""

        _LOGGER.debug("PollenStation from_dict %s", data)

        return PollenStation(
            name=data["name"],
            country_code=data["country_code"],
            distance_in_km=float(data["distance_in_km"]),
        )


@attr.s(auto_attribs=True, frozen=True)
class Allergen:
    """Class representing Allergen."""

    name: str
    latin_name: str
    level_number: int
    level_description: str

    @staticmethod
    def from_dict(data: List[Dict[str, Any]]) -> List["Allergen"]:
        """Transform data to dict."""

        _LOGGER.debug("Allergen from_dict %s", data)

        allergens = []
        for allergen in data:
            allergens.append(
                Allergen(
                    name=allergen["name"],
                    latin_name=allergen["latin_name"],
                    level_number=int(allergen["level_number"]),
                    level_description=allergen["level_description"],
                )
            )
        return allergens


@attr.s(auto_attribs=True, frozen=True)
class PollenForecast:
    """Class representing PollenForecast."""

    date: str
    allergens: List["Allergen"]

    @staticmethod
    def from_dict(data: List[Dict[str, Any]]) -> List["PollenForecast"]:
        """Transform data to dict."""

        _LOGGER.debug("PollenForecast from_dict %s", data)

        forecasts = []
        for forecast in data:
            forecast_allergens: List[Dict[str, Any]] = forecast["allergens"]
            forecasts.append(
                PollenForecast(
                    date=forecast["date"],
                    allergens=Allergen.from_dict(forecast_allergens),
                )
            )
        return forecasts


@attr.s(auto_attribs=True, frozen=True)
class PollenvarselResponse:
    """Class representing Pollenvarsel."""

    status: int
    pollen_station: "PollenStation"
    forecast: List["PollenForecast"]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PollenvarselResponse":
        """Transform data to dict."""

        _LOGGER.debug("PollenvarselResponse from_dict %s", data)

        forecast: List[Dict[str, Any]] = data["forecast"]
        pollen_station: Dict[str, Any] = data["pollen_station"]

        return PollenvarselResponse(
            status=data["status"],
            forecast=PollenForecast.from_dict(forecast),
            pollen_station=PollenStation.from_dict(pollen_station),
        )
