
from pydantic import BaseModel

class CountResetRequest(BaseModel):
    people_count: int

class MaxCountResetRequest(BaseModel):
    max_people_count: int