from datetime import datetime, timedelta
import secrets
import logging

from typing import Any

from aiohttp import ClientResponse
from .models.ring_configuration import RingConfiguration
from .models.daily_readiness import DailyReadiness

_LOGGER = logging.getLogger(__name__)

class OuraClient:
    def __init__(self, host: str, session, token: str):
        self._host = host
        self._session = session
        self._token = token
    
    async def make_request(self, method, url, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        headers["Authorization"] = f"Bearer {self._token}"
        response = await self._session.request(
            method, f"{self._host}/{url}", **kwargs, headers=headers,
        )
        return await response.json()

    async def async_get_data(self) -> list[Any]:
        data = []
        data.append(await self.async_get_ring_configuration()[0])
        data.append(await self.async_daily_readiness()[0])
        return data
    
    async def async_get_ring_configuration(self) -> list[RingConfiguration]:
        return {
            "id": "ring",
            "color": "stealth_black",
            "design": "balance",
            "firmware_version": "4.22.4",
            "hardware_type": "gen4",
            "set_up_at": "2024-11-11",
            "size": 13
        }
        data = await self.make_request("GET", f"ring_configuration")
        try:
            rings = [RingConfiguration(**a) for a in data['data']]
        except KeyError:
            _LOGGER.error("Failed to get ring from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return rings
    
    async def async_daily_readiness(self) -> list[DailyReadiness]:
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        data = await self.make_request("GET", f"daily_readiness?start_date={today.strftime('%Y-%m-%d')}&end_date={tomorrow.strftime('%Y-%m-%d')}")
        try:
            readiness = [DailyReadiness(**a) for a in data['data']]
        except KeyError:
            _LOGGER.error("Failed to get readiness from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return readiness
    
async def _raise_auth_or_response_error(response: dict[str, Any]) -> None:
    raise InvalidOuraAPIResponseError

class InvalidOuraAPIResponseError(Exception):
    """Error thrown when the external Oura API returns an invalid response."""

    def __init__(self, *args: object) -> None:
        """Initialise error."""
        super().__init__(*args)