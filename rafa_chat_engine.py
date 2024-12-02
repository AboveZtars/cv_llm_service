from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(model='gpt-4o-mini')
api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)
pinecone_index = pc.Index("rafa-data")
# load documents
# documents = SimpleDirectoryReader("data").load_data()
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, )
chat_engine = index.as_chat_engine(
    llm=client,
    chat_mode="context",
    system_prompt="You are a curricular bot that answers questions about Rafael Molina. A good backend developer from Venezuela."
)
