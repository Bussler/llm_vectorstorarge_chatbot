from typing import Union

from fastapi import FastAPI, BackgroundTasks, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from langchain.llms import HuggingFacePipeline
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

import transformers
import torch
import huggingface_hub

import uvicorn


app = FastAPI()


origins = [
    "http://localhost:5173",
]
chat_history = [[]]

class promt_request(BaseModel):
    q: str
    use_chat: int = 0

def setup_llm():
    model_id="bigscience/bloom-560m"
    device = f'cuda:{torch.cuda.current_device()}' if torch.cuda.is_available() else 'cpu'

    model_config = transformers.AutoConfig.from_pretrained(
        model_id,
    )

    model = transformers.AutoModelForCausalLM.from_pretrained(
        model_id,
        config=model_config,
        device_map=device,
    )
    
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_id,)

    # enable evaluation mode to allow model inference
    model.eval()
    print(f"Model loaded on {device}")

    stop_list = ['\nHuman:', '\n```\n']
    stop_token_ids = [tokenizer(x)['input_ids'] for x in stop_list]
    stop_token_ids = [torch.LongTensor(x).to(device) for x in stop_token_ids]

    # define custom stopping criteria object
    class StopOnTokens(transformers.StoppingCriteria):
        def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
            for stop_ids in stop_token_ids:
                if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                    return True
            return False

    stopping_criteria = transformers.StoppingCriteriaList([StopOnTokens()])

    generate_text = transformers.pipeline(
        model=model, 
        tokenizer=tokenizer,
        return_full_text=True,
        task='text-generation',
        # we pass model parameters here too
        stopping_criteria=stopping_criteria,
        temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
        max_new_tokens=64,  # max number of tokens to generate in the output
    )

    llm = HuggingFacePipeline(pipeline=generate_text)
    return llm


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    hugging_face_token = ''
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
    
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/query/")
def read_root(req: promt_request):
    result = app.qna({"question": req.q, "chat_history": chat_history[req.use_chat]})
    
    # M: store conversation in chat history:
    chat_history[req.use_chat].append((req.q, result["answer"]))
    
    return {result['answer']}

@app.get("/")
def read_root():
    return {"Hello": "World"}



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)