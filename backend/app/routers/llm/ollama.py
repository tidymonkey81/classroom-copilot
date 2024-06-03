# Import necessary libraries
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import ollama
from ollama import Client

router = APIRouter()
client = Client(host='http://localhost:11434')

class UserRequest(BaseModel):
    question: str
    model: str = "llama3"

@router.post("/ollama_text_prompt")
async def ollama_text_prompt(user_request: UserRequest):
    model_name = user_request.model
    question = user_request.question

    supported_models = ["llama2", "llama3", "mistral", "llama3"]
    if model_name not in supported_models:
        raise HTTPException(status_code=400, detail="Model not supported")

    messages = [{"role": "user", "content": question}]
    try:
        response = client.chat(model=model_name, messages=messages)
        if "message" in response and "content" in response["message"]:
            return {"model": model_name, "response": response["message"]["content"]}
        else:
            raise HTTPException(status_code=500, detail="Invalid response structure from model")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class Message(BaseModel):
    role: str
    content: str

class CopilotRequest(BaseModel):
    model: str
    messages: List[Message]
    options: Optional[Dict[str, float]] = None
    
@router.post("/ollama_copilot_prompt")
async def ollama_copilot_prompt(request: CopilotRequest):
    model_name = request.model
    messages = request.messages
    options = request.options or {}
    print(f"Model: {model_name}, Messages: {messages}, Options: {options}")

    try:
        print("Generating response...")
        response = ollama.chat(model=model_name, messages=messages, **options)
        print(f"Response: {response}")
        if "message" in response and "content" in response["message"]:
            print(f"Response: {response['message']['content']}")
            return {"model": model_name, "response": response["message"]["content"]}
        else:
            print(f"Invalid response structure from model: {response}")
            raise HTTPException(status_code=500, detail="Invalid response structure from model")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))