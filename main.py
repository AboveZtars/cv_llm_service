from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()


class Message(BaseModel):
    user_message: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/openai")
def get_openai_response(message: Message):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print(message.user_message)
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": message.user_message
                }
            ]
        )
        print(completion.choices[0].message)
        return {"response": completion.choices[0].message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
