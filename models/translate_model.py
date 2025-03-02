import pydantic


class TranslateInput(pydantic.BaseModel):
    user_input: str | None
    language_src: str | None
    language_target: str | None

class TranslateOutput(pydantic.BaseModel):
    translated_tex: str