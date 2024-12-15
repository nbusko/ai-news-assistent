from pydantic import BaseModel, model_validator, RootModel


class RAGContent(RootModel[dict[str, str]]):
    @model_validator(mode="after")
    def validate_content(cls, model):
        if not model.root:
            raise ValueError("JSON cannot be empty")

        for key, value in model.root.items():
            if not key.strip():
                raise ValueError("Keys cannot be empty or whitespace")
            if not value.strip():
                raise ValueError("Values cannot be empty or whitespace")

        return model


class RetrieveContent(BaseModel):
    content: str
    category: str
    topn: int = 10
