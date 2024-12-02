from pydantic import BaseModel

class HeartRate(BaseModel):
    bpm: int
    source: str
    timestamp: str

    @property
    def lookup(self):
        return "heartrate"