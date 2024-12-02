from pydantic import BaseModel

class DailyResilienceContributors:
    sleep_recovery: int
    daytime_recovery: int
    stress: int

class DailyResilience(BaseModel):
    id: str
    day: str
    level: str
    contributors: DailyResilienceContributors

    @property
    def lookup(self):
        return "daily_resilience"