from typing import Optional
from fastapi import FastAPI
import spacy

from models.phonetizer_model import PhonetizerInput

# Server init
app = FastAPI()

# NLP init
nlp = spacy.load('de_core_news_sm')

@app.post("/phonetizer")
async def get_phonetics(words: Optional[PhonetizerInput] = None):
    if not words.user_input:
        return
    doc = nlp(words.user_input)
    for token in doc:
        print(token.text, token.pos_, token.dep_)
    token = ' '.join([token.text for token in doc])
    return words

@app.post("/transcriber")
async def get_transcription(words: str):
    return words


# .\.venv\Scripts\pip.exe install spacy