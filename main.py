from typing import Optional, List
from fastapi import FastAPI
import jptranscription
import spacy

import models
import jptranscription

# Server init
app = FastAPI()

# NLP init
nlp = spacy.load('de_core_news_sm')

# Katakanizer init
katakanizer = jptranscription.Katakanizer()

# Transcription init
phonetics_transcriber = katakanizer.phonetics_transcriber

@app.post("/phonetizer", response_model=List[models.PhonetizerOutput])
async def get_phonetics(words: Optional[models.PhonetizerInput] = None) -> List[models.PhonetizerOutput]:
    if not words.user_input:
        return
    doc = nlp(words.user_input)
    words = []
    for token in doc:
        if token.pos_ == 'PUNCT':
            katakana_char = katakanizer.mapping[token.text + '\u0000']
        else:
            katakana_char, ipa = katakanizer.transcribe_word(token.text)
        words.append(models.PhonetizerOutput(word=token.text, katakana=katakana_char, ipa=ipa, pos=token.pos_))
    return words

@app.post("/transcriber")
async def get_transcription(words: str):
    return words
