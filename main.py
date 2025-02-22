from fastapi import FastAPI
from pydantic import BaseModel
import openai
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# Initialize the FastAPI app
app = FastAPI()

# CORS to allow frontend to make requests to the backend    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()
# Initialize the OpenAI client
#client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client =OpenAI()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Request model
class ChatRequest(BaseModel):
    message: str

# API route to handle the chat request
@app.post("/chat")
async def chat(request: ChatRequest):
    # Get the user's message from the request
    user_message = request.message
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use GPT model
        messages=[{"role": "user", "content": request.message}]
    )
    return {"reply": response["choices"][0]["message"]["content"]}


