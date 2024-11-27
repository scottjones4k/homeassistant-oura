"""Support for Oura sensors."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from typing import Any

from .const import (
    DOMAIN
)
from .api.models.ring_configuration import (
    RingConfiguration
)


ATTRIBUTION = "Data provided by Oura API"

class OuraBaseEntity(CoordinatorEntity):
    """Common base for Oura entities."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        idx,
        name
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, context=idx)
        self.idx = idx

        self._attr_device_info = DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, str(self.ring.id))},
            manufacturer="Oura",
            model=f"{self.ring.color.capitalize()} {self.ring.design.capitalize()} {self.ring.hardware_type.capitalize()} Ring",
            name=name,
        )

    @property
    def data(self) -> dict[str, Any]:
        """Shortcut to access coordinator data for the entity."""
        return self.coordinator.data[self.idx]
    
    @property
    def ring(self) -> RingConfiguration:
        """Shortcut to access coordinator data for the entity."""
        return self.coordinator.data["ring"]
    
    @property
    def available(self) -> bool:
        """Shortcut to access coordinator data for the entity."""
        return self.idx in self.coordinator.data
