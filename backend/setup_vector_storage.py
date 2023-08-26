from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import os
import uuid



def get_storage_count(db: Chroma):
    return db._collection.count()


def upsert(db: Chroma, embedder, documents):
    docs, ids = split_documents(documents)
    
    embed_docs = embedder.encode(docs)
    
    db._collection.upsert(ids=ids, embeddings=embed_docs, documents=docs)


def parse_documents(dir = "text_data/"):
    print("Parse in text documents...")
    loader = DirectoryLoader(dir, glob="**/*.txt" )
    documents = loader.load()
    return documents


def split_documents(documents):
    print("Doing text splitting...")
    text_splitter = CharacterTextSplitter(chunk_size = 100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents=documents)
    
    # M: Create ids according to page content
    namespace = uuid.NAMESPACE_URL
    ids = [str(uuid.uuid5(namespace, doc.page_content)) for doc in docs]
    return docs, ids


def setup_chroma_db(doc_directory = "./text_data/"):
    
    print("Load embeddings...")
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.isdir("./chroma_db"):
        print(f"Found data! Loading VectorDB...")
        
        doc_search = Chroma(persist_directory="./chroma_db", embedding_function=embedder)
    else:
        documents = parse_documents(doc_directory)
        docs, ids = split_documents(documents)
    
        print("Loading VectorDB...")
        doc_search = Chroma.from_documents(docs, embedder, ids=ids, persist_directory='./chroma_db')
        doc_search.persist()
    
    print(f"Elements in Storage: {get_storage_count(doc_search)}")
    
    return doc_search, embedder