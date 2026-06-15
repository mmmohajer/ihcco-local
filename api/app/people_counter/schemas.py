
from pydantic import BaseModel

class CountResetRequest(BaseModel):
    people_count: int