from pydantic import BaseModel

class DailyCardiovascularAge(BaseModel):
    day: str
    vascular_age: int

    @property
    def lookup(self):
        return "daily_cardiovascular_age"