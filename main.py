from typing import Optional, List
from fastapi import FastAPI
import jptranscription
import spacy

import models
from logic.inputhandler import InputHandler

# Server init
app = FastAPI()

# Input handler init
input_handler = InputHandler()

@app.post("/phonetizer")
async def get_phonetics(words: Optional[models.PhonetizerInput] = None):
    words = input_handler.get_phonetics(words)
    return words

@app.post("/transcriber")
async def get_transcription(words: Optional[models.PhonetizerInput] = None):
    words = input_handler.get_katakana(words)
    return words
