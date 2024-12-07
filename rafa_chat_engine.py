from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from prompts import system_prompt
import os

load_dotenv()
embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.embed_model = embed_model
client = OpenAI(model='gpt-4o-mini', max_tokens=100, temperature=0.3)
api_key = os.getenv("PINECONE_API_KEY")
# Load RAG
pc = Pinecone(api_key=api_key)
pinecone_index = pc.Index("rafa-data")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, )
# Chat
chat_engine = index.as_chat_engine(
    llm=client,
    chat_mode="context",
    system_prompt=system_prompt
)
