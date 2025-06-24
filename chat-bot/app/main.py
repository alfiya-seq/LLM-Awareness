# FastAPI backend

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow Streamlit frontend to call this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_API = "http://localhost:11434/api/generate"

@app.post("/chat/")
async def chat(request: Request):
    body = await request.json()
    user_prompt = body.get("prompt")
    user_model = body.get("model")

    response = requests.post(OLLAMA_API, json={
        "model": user_model,
        "prompt": user_prompt,
        "stream": False
    })

    result = response.json()
    return {"response": result.get("response")}
