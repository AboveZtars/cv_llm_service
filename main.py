from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from rafa_chat_engine import chat_engine

load_dotenv()

app = FastAPI()


class Message(BaseModel):
    user_message: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/openai")
def get_openai_response(message: Message):
    try:
        response = chat_engine.chat(
            "Da tu respuesta a mi mensaje enfocado en el Backend. Mensaje:" + message.user_message)
        return {"response": response.response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
