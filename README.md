# llm_vectorstorarge_chatbot
Chat with your own documents with models from huggingface, langchain and chromadb!  
The vector storage chromadb queries the relevant data at runtime and gives the appropriate context to the llm, which interprets the data.  
This enables you to efficiently search and summarize your documents with custom user prompts.

You can store your documents in `backend/text_data` to embed them at app startup or upload them through the frontend.  
After the documents are embedded into the vector database, they can be queried by user prompts.  
For simplicity, the relatively small `bigscience/bloom-560m` model is used at startup. The llm model can be changed through the frontend under the `Change LLM` menu.

## Backend
The backend opens a fastapi service at `http://localhost:8000`, which can be queried by the frontend.  

### Installation
Python is required for running the backend. A popular form of installation is through [anaconda](https://www.anaconda.com/), which also enables you to install the required libraries through the conda environment file.
Install the requirements (torch, huggingface transformers, langchain, chroma_db, sentence_transformers, fastapi) from the conda environment file in the `backend/` folder: `conda env create --file environment.yml`.  
Alternatively you can use [poetry](https://python-poetry.org/docs/) with the `pyproject.toml` file: `poetry install` to install the dependencies, then `poetry shell` to start the virtual environment.  
Furthermore create a [huggingface hub](https://huggingface.co) account and provide your access token in `hugging_face_token` in `backend/main.py`.

### Run Backend
In `backend/` start the backend with `python main.py`.  
The setup should start. This can take some time, since the model needs to be downloaded from huggingface and the vectorstorage needs to be built.  
After setup, the backend can be queried at `http://localhost:8000/query/?q=<user query>`.  
A swagger documentation of all available routes can be found at `http://localhost:8000/docs/`.  

## Frontend
Responsible for getting user input and invoking query requests to the llm.

### Installation
[Nodejs](https://nodejs.org/de) is required for building and running the frontend.  
Install the requirements (Vue, PrimeVue, Axios) by going to `frontend/min-example` and execute `npm install`.

### Run Frontend
Make sure that the backend is up and running.  
In `frontend/min-example/` execute `npm run dev`. The service should start on `http://localhost:5173/`.  
Under the `Query` menu, you can upload new text documents, query the embedded documents and manage chat histories.  
In the `Change LLM` menu, you can change the currently used llm model by providing a model_id from [huggingface hub](https://huggingface.co/models).