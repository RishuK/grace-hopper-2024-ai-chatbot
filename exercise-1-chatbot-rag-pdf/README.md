# grace-hopper-2024-ai-chatbot
## Grace Hopper AI Chatbot application

### Pre-requisites start here

#### Step 1: Initiatize poetry project
```bash
poetry init
```
### Step 2: Install the Dependencies:

- langchain
- streamlit - used for building POCs/prototypes
- streamlit-chat
- pypdf
- chromadb
- fastembed

```bash
pip3 install langchain langchain_community streamlit streamlit_chat chromadb pypdf fastembed
```
### Step 3: Set up Ollama
We need a LLM server which we can easily setup locally and do not have to worry about API keys!

To do this, download Ollama from https://ollama.com/
Ollama can be setup locally and provides multiple models: https://ollama.com/library

We can run a compact model - Mistral-7B or Llama3
<more to come here depending on the model we choose"

```
ollama pull mistral
```

### Pre-requisites end here

### Excercise execution

#### Building RAG chat-bot 
We will build a RAG-based chat application which will answer questions based on PDF document you will upload. 
We will use Langchain, [Ollama](https://ollama.com/) and Streamlit UI


#### Let's build the RAG pipeline
The RAG pipeline is divided into the following steps which will be achieved from the following file
```
rag_pipeline.py
```
1. Upload document - use Elena.pdf already provided in the folder
2. Split the document into smaller chunks using [text splitters](https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/)
3. Vectorize the document chunks using [FastEmeddings](https://github.com/qdrant/fastembed) and store in [Chroma](https://github.com/chroma-core/chroma)
4. Configure the Vector store [Retriever](https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/vectorstore/) for the type of search
5. Construct langchain conversion chain using [LECL](https://python.langchain.com/v0.1/docs/expression_language/) (LangChain Expression Language)

#### StreamLit UI
Use StreamLit APIs to demonstrate the chatbot
```
chat_ui.py
```

#### How to run this StreamLit app?
Execute 
```
streamlist run chat_ui.py
```

Use the pdf file - Elena.pdf in the folder and Ask questions about Elena's work





