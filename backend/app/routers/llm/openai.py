from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from openai import OpenAI
import os
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

class Message(BaseModel):
    role: str
    content: str

class CopilotRequest(BaseModel):
    model: str
    messages: List[Message]
    options: Optional[Dict[str, float]] = None

@router.post("/openai_copilot_prompt")
async def openai_copilot_prompt(request: CopilotRequest):
    logging.info("Received request: %s", request.model_dump_json())
    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
            **(request.options or {})
        )
        logging.info("Received response: %s", response)
        return {"model": request.model, "response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
