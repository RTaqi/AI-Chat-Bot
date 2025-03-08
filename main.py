from fastapi import FastAPI
from pydantic import BaseModel
from mistralai.client import MistralClient
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
# client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# client =OpenAI()  THIS IS MAIN USE IN OPEN AI KEY
# openai.api_key = os.getenv("OPENAI_API_KEY")

# MISTRAL API KEY
API_KEY = os.getenv("OPENAI_API_KEY")
client = MistralClient(api_key=API_KEY)


# Request model
class ChatRequest(BaseModel):
    message: str

# API route to handle the chat request
# @app.post("/chat")
# async def chat(request: ChatRequest):
#     # Get the user's message from the request
#     user_message = request.message
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",  # Use GPT model
#         messages=[{"role": "user", "content": request.message}]
#     )
#     return {"reply": response["choices"][0]["message"]["content"]}


# MISTRAL AI AGEN
SYSTEM_PROMPT= "You are a professional AI English Language Tutor. Answer concisely and professionally help\
     user to in correcting their mistakes. You role is to rectify grammer, tense and conversation. \
         Mention mistakes any reply with correct sentence.\
            Start conversation with that is 'Hello! Welcome to our online AI based English Language Bot.\
                Start conversation so I can help you.'"

@app.post("/chat")
async def chat(request: ChatRequest):
    response = client.chat(
        model="mistral-7b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},  # System prompt
            {"role": "user", "content": request.user_input}
        ]
    )
    return {"response": response.choices[0].message["content"]}


