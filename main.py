from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from rafa_chat_engine import chat_engine
from fastapi.middleware.cors import CORSMiddleware
from prompts import context_input_prompt

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    user_message: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/openai")
def get_openai_response(message: Message):
    try:
        response = chat_engine.chat(
            context_input_prompt + message.user_message)
        return {"response": response.response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
