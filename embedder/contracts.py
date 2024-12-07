from pydantic import BaseModel


class UserRequest(BaseModel):
    """Contract for user req"""

    text: str