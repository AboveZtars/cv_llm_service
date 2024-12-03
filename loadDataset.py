from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from dotenv import load_dotenv
import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()
embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.embed_model = embed_model
client = OpenAI(model='gpt-4o-mini')
api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=api_key)
pinecone_index = pc.Index("rafa-data")
# load documents
documents = SimpleDirectoryReader("data").load_data()
vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(
    vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    embed_model=embed_model, storage_context=storage_context, documents=documents)
