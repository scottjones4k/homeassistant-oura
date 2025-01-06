from pydantic import BaseModel

class DailyResilienceContributors(BaseModel):
    sleep_recovery: float
    daytime_recovery: float
    stress: float

class DailyResilience(BaseModel):
    id: str
    day: str
    level: str
    contributors: DailyResilienceContributors

    @property
    def lookup(self):
        return "daily_resilience"