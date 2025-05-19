from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

TOGETHER_API_KEY = "31fb60f687ee77df150a631c7b8b3bb7d4ac8902fba9aa8831ffec9d6c1b7c9a"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str

@app.post("/api/ask")
async def ask(body: AskRequest):
    question = body.question

    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.9,
        "messages": [
            { "role": "system", "content": "You are a helpful assistant for quality engineering work instructions." },
            { "role": "user", "content": question }
        ]
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", json=data, headers=headers)
    result = response.json()

    # Check and return the assistant's message
    if "choices" in result and len(result["choices"]) > 0:
        answer = result["choices"][0]["message"]["content"]
        return { "answer": answer }
    else:
        return { "error": result }