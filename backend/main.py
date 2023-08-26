from typing import Union

from fastapi import FastAPI, BackgroundTasks, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

import huggingface_hub

import uvicorn

from setup_model import setup_llm


app = FastAPI()


origins = [
    "http://localhost:5173",
]
chat_history = [[]]

class promt_request(BaseModel):
    q: str
    use_chat: int = 0
    

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    hugging_face_token = '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'
    huggingface_hub.login(token=hugging_face_token)
    
    print("Set up llm")
    app.llm = setup_llm()
    
    print("parse in text documents")
    loader = DirectoryLoader("text_data/", glob="**/*.txt" )
    documents = loader.load()
    
    print("doing text splitting")
    text_splitter = CharacterTextSplitter(chunk_size = 100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents=documents)
    
    print("embeddings")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("vector store")
    app.doc_search = Chroma.from_documents(docs, embeddings, persist_directory='chroma_db')
    
    app.qna = ConversationalRetrievalChain.from_llm(
        app.llm, 
        app.doc_search.as_retriever(), 
        return_source_documents=True
    )
    
    yield
    
    # Clean up the ML models and release the resources
    del app.llm
    del app.doc_search
    del app.qna
    
    
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/query/")
def read_root(req: promt_request):
    
    if len(chat_history) == req.use_chat:
        chat_history.append([])
    
    result = app.qna({"question": req.q, "chat_history": chat_history[req.use_chat]})
    
    # M: store conversation in chat history:
    chat_history[req.use_chat].append((req.q, result["answer"]))
    
    return {result['answer']}


@app.get("/history/")
def get_history():    
    
    return chat_history


@app.get("/history/{h_id}/reset/")
def reset_history(h_id: int):    
    if len(chat_history) < h_id or h_id < 0:
        return {'success': 400, 'message': 'illegal h_id'}
    
    chat_history[h_id] = []
    
    return {'success': 200}


@app.get("/")
def read_root():
    return {"Hello": "World"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)