from datetime import datetime, timedelta
import secrets
import logging

from typing import Any

from aiohttp import ClientResponse
from .models.ring_configuration import RingConfiguration
from .models.daily_readiness import DailyReadiness
from .models.daily_resilience import DailyResilience
from .models.daily_sleep import DailySleep
from .models.daily_stress import DailyStress
from .models.heartrate import HeartRate
from .models.daily_cardiovascular_age import DailyCardiovascularAge
from .models.personal_info import PersonalInfo
from .models.daily_activity import DailyActivity

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
        data.append(await self.async_daily_readiness())
        data.append(await self.async_daily_resilience())
        data.append(await self.async_daily_sleep())
        data.append(await self.async_daily_stress())
        data.append(await self.async_heartrate())
        data.append(await self.async_cardiovascular_age())
        data.append(await self.async_personal_info())
        data.append(await self.async_activity())
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
    
    async def async_daily_readiness(self) -> DailyReadiness:
        data = await self.make_request("GET", "daily_readiness", params=build_date_params())
        try:
            readiness = DailyReadiness(**data['data'][-1]) 
        except IndexError:
            _LOGGER.warning("Failed to get readiness from Oura API: %s", str(data))
        except KeyError:
            _LOGGER.error("Failed to get readiness from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return readiness
    
    async def async_daily_resilience(self) -> DailyResilience:
        data = await self.make_request("GET", "daily_resilience", params=build_date_params())
        try:
            resilience = DailyResilience(**data['data'][-1])
        except IndexError:
            _LOGGER.warning("Failed to get resilience from Oura API: %s", str(data))
        except KeyError:
            _LOGGER.error("Failed to get resilience from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return resilience
    
    async def async_daily_sleep(self) -> DailySleep:
        data = await self.make_request("GET", "daily_sleep", params=build_date_params())
        try:
            sleep = DailySleep(**data['data'][-1])
        except IndexError:
            _LOGGER.warning("Failed to get sleep from Oura API: %s", str(data))
        except KeyError:
            _LOGGER.error("Failed to get sleep from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return sleep
    
    async def async_daily_stress(self) -> DailyStress:
        data = await self.make_request("GET", "daily_stress", params=build_date_params())
        try:
            stress = DailyStress(**data['data'][-1])
        except IndexError:
            _LOGGER.warning("Failed to get stress from Oura API: %s", str(data))
        except KeyError:
            _LOGGER.error("Failed to get stress from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return stress
    
    async def async_heartrate(self) -> HeartRate:
        data = await self.make_request("GET", "heartrate", params=build_datetime_params())
        try:
            heartrate = HeartRate(**data['data'][-1])
        except IndexError:
            _LOGGER.warning("Failed to get heart rate from Oura API: %s", str(data))
        except KeyError:
            _LOGGER.error("Failed to get heart rate from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return heartrate
    
    async def async_cardiovascular_age(self) -> DailyCardiovascularAge:
        data = await self.make_request("GET", "daily_cardiovascular_age", params=build_date_params())
        try:
            age = DailyCardiovascularAge(**data['data'][-1])
        except IndexError:
            _LOGGER.warning("Failed to get cardiovascular age from Oura API: %s", str(data))
        except KeyError:
            _LOGGER.error("Failed to get cardiovascular age from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return age
    
    async def async_personal_info(self) -> PersonalInfo:
        data = await self.make_request("GET", "personal_info")
        try:
            info = PersonalInfo(**data)
        except IndexError:
            _LOGGER.warning("Failed to get personal info from Oura API: %s", str(data))
        except KeyError:
            _LOGGER.error("Failed to get personal info from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return info
    
    async def async_activity(self) -> DailyActivity:
        data = await self.make_request("GET", "daily_activity")
        try:
            activity = DailyActivity(**data['data'][-1])
        except IndexError:
            _LOGGER.warning("Failed to get activity from Oura API: %s", str(data))
        except KeyError:
            _LOGGER.error("Failed to get activity from Oura API: %s", str(data))
            _raise_auth_or_response_error(data)
        return activity
    
def build_date_params():
    today = datetime.today()
    yesterday = today + timedelta(days=-1)
    tomorrow = today + timedelta(days=1)
    return {
        "start_date": yesterday.strftime('%Y-%m-%d'),
        "end_date": tomorrow.strftime('%Y-%m-%d')
    }

def build_datetime_params():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    return {
        "start_datetime": today.strftime('%Y-%m-%d'),
        "end_datetime": tomorrow.strftime('%Y-%m-%d')
    }

async def _raise_auth_or_response_error(response: dict[str, Any]) -> None:
    raise InvalidOuraAPIResponseError

class InvalidOuraAPIResponseError(Exception):
    """Error thrown when the external Oura API returns an invalid response."""

    def __init__(self, *args: object) -> None:
        """Initialise error."""
        super().__init__(*args)