from datetime import datetime, timedelta
import secrets
import logging

from typing import Any

from aiohttp import ClientResponse
from .models.ring_configuration import RingConfiguration
from .models.daily_readiness import DailyReadiness
from .models.daily_resilience import DailyResilience
from .models.daily_sleep import DailySleep

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
        data.extend(await self.async_get_ring_configuration())
        data.extend(await self.async_daily_readiness())
        data.extend(await self.async_daily_resilience())
        return data
    
    async def async_get_ring_configuration(self) -> list[RingConfiguration]:
        return [RingConfiguration(**{
            "id": "ring",
            "color": "stealth_black",
            "design": "balance",
            "firmware_version": "4.22.4",
            "hardware_type": "gen4",
            "set_up_at": "2024-11-11",
            "size": 13
        })]
        data = await self.make_request("GET", f"ring_configuration?start_date={today.strftime('%Y-%m-%d')}&end_date={tomorrow.strftime('%Y-%m-%d')}")
        try:
            rings = [RingConfiguration(**a) for a in data['data']]
        except KeyError:
            _LOGGER.error("Failed to get ring from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return rings
    
    async def async_daily_readiness(self) -> list[DailyReadiness]:
        data = await self.make_request("GET", "daily_readiness", params=build_params())
        try:
            readiness = [DailyReadiness(**a) for a in data['data']]
        except KeyError:
            _LOGGER.error("Failed to get readiness from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return readiness
    
    async def async_daily_resilience(self) -> list[DailyResilience]:
        data = await self.make_request("GET", "daily_resilience", params=build_params())
        try:
            resilience = [DailyResilience(**a) for a in data['data']]
        except KeyError:
            _LOGGER.error("Failed to get resilience from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return resilience
    
    async def async_daily_resilience(self) -> list[DailySleep]:
        data = await self.make_request("GET", "daily_sleep", params=build_params())
        try:
            sleep = [DailySleep(**a) for a in data['data']]
        except KeyError:
            _LOGGER.error("Failed to get sleep from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return sleep
    
def build_params():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    return {
        "start_date": today.strftime('%Y-%m-%d'),
        "end_date": tomorrow.strftime('%Y-%m-%d')
    }

async def _raise_auth_or_response_error(response: dict[str, Any]) -> None:
    raise InvalidOuraAPIResponseError

class InvalidOuraAPIResponseError(Exception):
    """Error thrown when the external Oura API returns an invalid response."""

    def __init__(self, *args: object) -> None:
        """Initialise error."""
        super().__init__(*args)