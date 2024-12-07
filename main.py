from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from dotenv import load_dotenv
from rafa_chat_engine import chat_engine
from fastapi.middleware.cors import CORSMiddleware
from prompts import context_input_prompt
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


load_dotenv()

limiter = Limiter(key_func=get_remote_address,  default_limits=["1/minute"])
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class Message(BaseModel):
    user_message: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/openai")
@limiter.limit("5/30seconds")
async def get_openai_response(request: Request, response: Response):
    try:
        # Parse the JSON body from the request
        body: Message = await request.json()
        user_message = body.user_message

        if not user_message:
            raise HTTPException(
                status_code=400, detail="user_message is required")

        response = chat_engine.chat(
            context_input_prompt + user_message)

        # Log the response
        print(f"Response: {response.response}")
        return {"response": response.response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
