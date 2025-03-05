import pydantic
from enum import Enum

class Language(Enum):
    GERMAN = 'de'
    JAPANESE = 'ja'

class TranslateEngine(Enum):
    GOOGLETRANSLATE = 1
    CHATGPT = 2

class InputModel(pydantic.BaseModel):
    input_text: str | None
    src_lang: Language | None
    target_lang: Language | None

class OutputModel(pydantic.BaseModel):
    input_text: list[str] | None
    input_text_phonetics: list[str] | None
    output_text: list[str] | None
    output_text_phonetics: list[str] | None
    