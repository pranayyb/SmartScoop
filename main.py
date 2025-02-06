import os
import warnings
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from SmartScoop.app import ShoppingAssistantApp
from dotenv import load_dotenv
import uvicorn

warnings.filterwarnings("ignore")
load_dotenv()

# Load configuration
config = {
    "db_name": os.getenv("DB_NAME", "shopping_assistant.db"),
    "AMAZON_API_KEY": os.getenv("AMAZON_API_KEY"),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
}

# Initialize FastAPI app
app = FastAPI()
shopping_assistant = ShoppingAssistantApp(config)


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await shopping_assistant.handle_message(
            request.user_id, request.message
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=True
    )
