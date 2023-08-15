# llm_vectorstorarge_chatbot
Chat with your own documents with models from huggingface, langchain and chromadb!  
The vector storage chromadb queries the relevant data at runtime and gives the appropriate context to the llm, which interprets the data.  
Store your documents in `backend/text_data` and query them through the Vuejs frontend.

## Backend
The backend opens a fastapi service at `http://localhost:8000`, which can be queried by the frontend.
For simplicity, the relatively small `bigscience/bloom-560m"` model is used, this can be changed by setting the `model_id` parameter in `backend/main.py`.

### Installation
Install the requirements (torch, huggingface transformers, langchain, chroma_db, sentence_transformers, fastapi) from the conda environment file: `conda env create --file environment.yaml`.  
Furthermore create a huggingface hub account and provide your access token in `hugging_face_token` in `backend/main.py`.

### Run Backend
In `backend/` start the backend with `python main.py`.  
The setup should start. This can take a time, since the model needs to be downloaded from huggingface and the vectorstorage needs to be built.  
After setup, the backend can be queried at `http://localhost:8000/query/?q=`...

## Frontend
Responsible for getting user input and invoking query requests to the llm.

### Installation
Install the requirements (Vue, PrimeVue, Axios) by going to `frontend/min-example` and execute `npm install`.

### Run Frontend
Make sure that the backend is up and running.  
In `frontend/min-example/` execute `npm run dev`. The service should start on `http://localhost:5173/`.