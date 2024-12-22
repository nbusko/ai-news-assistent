from pydantic import BaseModel
from typing import List

class UserRequest(BaseModel):
    """Contract for user req"""
    texts: List[str]