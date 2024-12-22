from pydantic import BaseModel

class RequestData(BaseModel):
    query: str
