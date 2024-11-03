from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from logic.inputhandler import InputHandler

# Server init
app = FastAPI()

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

@app.post("/transcriber")
async def get_transcription(words: Optional[models.PhonetizerInput] = None):
    words = input_handler.get_katakana(words)
    return words
