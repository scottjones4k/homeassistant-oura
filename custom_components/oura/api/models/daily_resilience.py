from pydantic import BaseModel

class DailyResilience(BaseModel):
    id: str
    day: str
    level: str

    @property
    def lookup(self):
        return "daily_resilience"