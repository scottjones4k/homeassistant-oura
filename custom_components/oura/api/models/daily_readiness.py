from pydantic import BaseModel

class DailyReadiness(BaseModel):
    id: str
    day: str
    score: int
    temperature_deviation: int
    temperature_trend_deviation: int
    timestamp: str

    @property
    def lookup(self):
        return "daily_readiness"