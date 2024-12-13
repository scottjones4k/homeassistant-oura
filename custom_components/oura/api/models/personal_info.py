from pydantic import BaseModel

class PersonalInfo(BaseModel):
    id: str
    age: int
    weight: float
    height: float
    biological_sex: str

    @property
    def lookup(self):
        return "personal_info"