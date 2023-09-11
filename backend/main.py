from typing import Union, List
import os

from fastapi import FastAPI, BackgroundTasks, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
import huggingface_hub

from setup_model import setup_llm
from setup_vector_storage import (
    setup_chroma_db,
    add_document,
    get_storage_count,
    get_storage_documents,
    delete_document,
)


app = FastAPI()


origins = [
    "http://localhost:5173",
]
chat_history = [[]]


class promt_request(BaseModel):
    q: str
    use_chat: int = 0


class model_name(BaseModel):
    model_id: str


class document_sources(BaseModel):
    documents: List[str]

def setup_llm_model(model_id="bigscience/bloom-560m"):
    app.llm = setup_llm(model_id)
    app.qna = ConversationalRetrievalChain.from_llm(
        app.llm, app.doc_search.as_retriever(), return_source_documents=True
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    hugging_face_token = os.environ.get("HUGGINGFACE_TOKEN")
    huggingface_hub.login(token=hugging_face_token)

    app.doc_search, app.embedder = setup_chroma_db()

    # M: TODO test kwargs: load more docs with k    
    setup_llm_model(model_id="bigscience/bloom-560m")

    yield

    # Clean up the ML models and release the resources
    del app.llm
    del app.doc_search
    del app.embedder
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

    return {result["answer"]}


@app.post("/query/llm/")
def load_model(model_name: model_name):
    try:
        setup_llm_model(model_id=model_name.model_id)

    except Exception as e:
        return {
            "success": 400,
            "message": f"There was an error loading a new model! {str(e)}",
        }

    return {"success": 200}


@app.get("/query/llm/")
def get_model():
    return {"success": 200, "model_id": app.llm.pipeline.model.name_or_path}


@app.get("/history/")
def get_history():
    return chat_history


@app.get("/history/{h_id}/reset/")
def reset_history(h_id: int):
    if len(chat_history) < h_id or h_id < 0:
        return {"success": 400, "message": "illegal h_id"}

    chat_history[h_id] = []

    return {"success": 200}


@app.post("/vectordb/add/")
def add_file_vectordb(files: List[UploadFile] = File(...)):
    try:
        add_document(app, files)
    except Exception as e:
        return {
            "success": 400,
            "message": f"There was an error uploading a file! {str(e)}",
        }
    finally:
        for file in files:
            file.file.close()
    return {"success": 200}


@app.post("/vectordb/delete/")
def delete_file_vectordb(files: document_sources):
    delete_document(app.doc_search, files.documents)
    return {"success": 200}


@app.get("/vectordb/documents/")
def get_files_vectordb():
    docs = get_storage_documents(app.doc_search)
    return {"success": 200, "docs": docs}


@app.get("/vectordb/documents_count/")
def get_file_count_vectordb():
    docs_count = get_storage_count(app.doc_search)
    return {"success": 200, "docs_count": docs_count}


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
