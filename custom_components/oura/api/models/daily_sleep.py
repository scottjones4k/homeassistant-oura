from pydantic import BaseModel

class DailySleep(BaseModel):
    id: str
    day: str
    score: int
    timestamp: str

    @property
    def lookup(self):
        return "daily_sleep"