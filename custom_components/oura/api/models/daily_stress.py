from pydantic import BaseModel

class DailyStress(BaseModel):
    id: str
    stress_high: int
    recovery_high: int
    day: str
    day_summary: str | None

    @property
    def lookup(self):
        return "daily_stress"