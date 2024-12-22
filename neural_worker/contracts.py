from pydantic import BaseModel, constr, Field
from typing import List, Literal


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: constr(min_length=1)


class WorkerRequest(BaseModel):
    messages: List[Message]
    max_new_tokens: int = Field(
        default=512,
        title="Max new generated tokens",
    )