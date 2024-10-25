from pydantic import BaseModel


class PhonetizerInput(BaseModel):
    user_input: str | None
