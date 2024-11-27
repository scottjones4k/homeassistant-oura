from pydantic import BaseModel

class RingConfiguration(BaseModel):
    id: str
    color: str
    design: str
    firmware_version: str
    hardware_type: str
    set_up_at: str
    size: int

    @property
    def lookup(self):
        return "ring"