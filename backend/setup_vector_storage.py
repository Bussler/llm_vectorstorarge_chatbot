from langchain.vectorstores import Chroma
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import os



def get_storage_count(db: Chroma):
    return db._collection.count()


def parse_documents(dir = "text_data/"):
    print("Parse in text documents...")
    loader = DirectoryLoader(dir, glob="**/*.txt" )
    documents = loader.load()
    return documents


def split_documents(documents):
    print("Doing text splitting...")
    text_splitter = CharacterTextSplitter(chunk_size = 100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents=documents)
    return docs


def setup_chroma_db(doc_directory = "./text_data/"):
    
    print("Load embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    if os.path.isdir("./chroma_db"):
        print(f"Found data! Loading VectorDB...")
        
        doc_search = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    else:
        documents = parse_documents(doc_directory)
        docs = split_documents(documents)
    
        print("Loading VectorDB...")
        doc_search = Chroma.from_documents(docs, embeddings, persist_directory='./chroma_db')
    
    print(f"Elements in Storage: {get_storage_count(doc_search)}")
    
    return doc_search