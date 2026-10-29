from pydantic import BaseModel, Field, field_validator


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Question must not be blank.")
        return value.strip()


class AskResponse(BaseModel):
    answer: str
    disclaimer: str = (
        "Educational use only. Not a diagnosis or treatment recommendation. "
        "Consult a qualified healthcare professional for personal medical advice."
    )
