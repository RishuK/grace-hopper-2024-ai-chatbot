# grace-hopper-2024-ai-chatbot
## Grace Hopper AI Chatbot application

## Workspace setup

### Steps: 
#### Install pip, python, poetry
python version: 3.12.5
pip3

#### Initiatize poetry project
```bash
poetry init
```

#### Prepare yourself with concepts 
What is RAG?
What is LLM?
What is vector DB? 
What are embeddings? 

## Building RAG chat-bot 
We will build a RAG-based chat application which will answer questions based on PDF document you will upload. 
We will use Langchain, [Ollama](https://ollama.com/) and Streamlit UI

### Dependencies:

- langchain
- streamlit - used for building POCs/prototypes 
- streamlit-chat
- pypdf
- chromadb
- fastembed

### Install all dependencies
```bash
pip3 install langchain langchain_community streamlit streamlit_chat chromadb pypdf fastembed
```
### Set up Ollama
We need a LLM server which we can easily setup locally and do not have to worry about API keys!

To do this, download Ollama from https://ollama.com/ 
Ollama can be setup locally and provides multiple models: https://ollama.com/library

We can run a compact model - Mistral-7B or Llama3
<more to come here depending on the model we choose" 

```
ollama pull mistral
```
### Let's build the RAG pipeline
The RAG pipeline is divided into the following steps which will be achieved from the following file
```
rag_pipeline.py
```
1. Upload document 
2. Split the document into smaller chunks
3. Vectorize the document chunks using FastEmeddings and store in Chroma
4. Configure the Vector store Retriever for the type of search
5. Construct langchain conversion chain using LECL (LangChain Expression Language)

#### StreamLit UI
Use StreamLit APIs to demonstrate the chat bot
```
chat_ui.py
```






