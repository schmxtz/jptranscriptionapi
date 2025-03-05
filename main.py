from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator

import models
from logic.inputhandler import InputHandler
from models.input_model import *

# Server init
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# Add CORS middleware for frontend
origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input handler init
input_handler = InputHandler()

translate_engines = {
    TranslateEngine.GOOGLETRANSLATE: GoogleTranslator()
}

def translate(engine, source, target, text):
    translate_engine = translate_engines[engine]
    translate_engine.source = source
    translate_engine.target = target
    return translate_engine.translate(text)

@app.post("transcriblate")
async def post_transcriblate(user_input: Optional[models.InputModel] = None):
    if not user_input: return
    if not user_input.input_text: return



@app.post("/transcriber")
async def get_transcription(words: Optional[models.PhonetizerInput] = None):
    words = input_handler.get_katakana(words)
    return words

@app.post("/translate")
async def get_translation(translate_input: Optional[models.InputModel] = None):
    user_input = translate_input.user_input
    src = translate_input.language_src
    target = translate_input.language_target
    if user_input and src in supported_lang and target in supported_lang and src != target:
        return GoogleTranslator(source='auto', target=target).translate(user_input)
    return ''
        
