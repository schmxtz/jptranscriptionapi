import pydantic


class PhonetizerInput(pydantic.BaseModel):
    user_input: str | None

class PhonetizerOutput(pydantic.BaseModel):
    word: str
    katakana: str
    ipa: str | None
    pos: str