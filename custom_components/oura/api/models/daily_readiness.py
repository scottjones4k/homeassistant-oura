from pydantic import BaseModel

class ReadinessContributors(BaseModel):
    activity_balance: int
    body_temperature: int
    hrv_balance: int
    previous_day_activity: int
    previous_night: int
    recovery_index: int
    resting_heart_rate: int
    sleep_balance: int

class DailyReadiness(BaseModel):
    id: str
    day: str
    score: int
    temperature_deviation: float
    temperature_trend_deviation: float
    timestamp: str
    contributors: ReadinessContributors

    @property
    def lookup(self):
        return "daily_readiness"