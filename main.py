from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI

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
        client = OpenAI(model='gpt-4o-mini')

        documents = SimpleDirectoryReader("data").load_data()

        index = VectorStoreIndex.from_documents(documents)
        chat_engine = index.as_chat_engine(
            chat_mode="context",
            system_prompt=(
                "You are a curricular bot that answers questions about Rafael Molina."
                " A good backend developer from Venezuela."
            ), llm=client)
        response = chat_engine.chat(message.user_message)

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
