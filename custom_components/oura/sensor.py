"""Support for YBC sensors."""
from __future__ import annotations

import logging
import voluptuous as vol
from typing import Any, Optional
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from homeassistant.components.sensor import SensorEntity, SensorStateClass, SensorDeviceClass, SensorEntityDescription, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers import entity_platform
from homeassistant.helpers.typing import StateType
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
from homeassistant.util import dt as dt_util
from .const import (
    DOMAIN
)

from .oura_update_coordinator import OuraUpdateCoordinator
from .entity import OuraBaseEntity

_LOGGER = logging.getLogger(__name__)

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
@dataclass(frozen=True, kw_only=True)
class OuraSensorEntityDescription(SensorEntityDescription):
    """Describes Oura sensor entity."""

    value_fn: Callable[[dict[str, Any]], StateType]

DAILY_SENSORS = (
    OuraSensorEntityDescription(
        key="daily_readiness",
        translation_key="daily_readiness",
        value_fn=lambda data: data.score,
        state_class=SensorStateClass.MEASUREMENT
    ),
    OuraSensorEntityDescription(
        key="daily_resilience",
        translation_key="daily_resilience",
        value_fn=lambda data: data.level
    ),
    OuraSensorEntityDescription(
        key="daily_sleep",
        translation_key="daily_sleep",
        value_fn=lambda data: data.score,
        state_class=SensorStateClass.MEASUREMENT
    ),
    OuraSensorEntityDescription(
        key="daily_stress",
        translation_key="daily_stress",
        value_fn=lambda data: data.stress_high,
        state_class=SensorStateClass.MEASUREMENT
    ),
    OuraSensorEntityDescription(
        key="heartrate",
        translation_key="heartrate",
        value_fn=lambda data: data.bpm,
        state_class=SensorStateClass.MEASUREMENT
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Oura sensor platform."""
    coordinator: OuraUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    name: str = hass.data[DOMAIN][config_entry.entry_id]["name"]

    await coordinator.async_config_entry_first_refresh()

    sensors = [
        OuraSensor(
            coordinator,
            entity_description,
            name
        )
        for entity_description in DAILY_SENSORS
    ]

    async_add_entities(sensors) 

class OuraSensor(OuraBaseEntity, SensorEntity):
    """Representation of a Oura sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entity_description,
        name
    ) -> None:
        """Initialize the sensor."""
        idx = entity_description.key
        super().__init__(coordinator, idx, name)

        self.entity_description = entity_description

        self._attr_unique_id = f"{self.idx}_{self.entity_description.key}"

    @property
    def native_value(self) -> StateType:
        """Return the state."""

        try:
            state = self.entity_description.value_fn(self.data)
        except (KeyError, ValueError):
            return None

        return state
    
    @property
    def extra_state_attributes(self):
        """Returns the sensor attributes."""
        match self.entity_description.key:
            case "daily_readiness":
                return {
                    "activity_balance": self.data.contributors.activity_balance,
                    "body_temperature": self.data.contributors.body_temperature,
                    "hrv_balance": self.data.contributors.hrv_balance,
                    "previous_day_activity": self.data.contributors.previous_day_activity,
                    "previous_night": self.data.contributors.previous_night,
                    "recovery_index": self.data.contributors.recovery_index,
                    "resting_heart_rate": self.data.contributors.resting_heart_rate,
                    "sleep_balance": self.data.contributors.sleep_balance
                }
            case "daily_sleep":
                return {
                    "deep_sleep": self.data.contributors.deep_sleep,
                    "efficiency": self.data.contributors.efficiency,
                    "latency": self.data.contributors.latency,
                    "rem_sleep": self.data.contributors.rem_sleep,
                    "restfulness": self.data.contributors.restfulness,
                    "timing": self.data.contributors.timing,
                    "total_sleep": self.data.contributors.total_sleep
                }
            case "daily_resilience":
                return {
                    "sleep_recovery": self.data.contributors.sleep_recovery,
                    "daytime_recovery": self.data.contributors.daytime_recovery,
                    "stress": self.data.contributors.stress
                }
            case _:
                return {}
        return self._attributes