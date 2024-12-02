from pydantic import BaseModel

class DailySleepContributors:
    deep_sleep: int
    efficiency: int
    latency: int
    rem_sleep: int
    restfulness: int
    timing: int
    total_sleep: int

class DailySleep(BaseModel):
    id: str
    day: str
    score: int
    timestamp: str
    contributors: DailySleepContributors

    @property
    def lookup(self):
        return "daily_sleep"