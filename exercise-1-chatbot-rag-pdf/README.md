# grace-hopper-2024-ai-chatbot
## Grace Hopper AI Chatbot application

### Pre-requisites start here

#### Initiatize poetry project
```bash
poetry init
```
### Install the Dependencies:

- langchain
- streamlit - used for building POCs/prototypes
- streamlit-chat
- pypdf
- chromadb
- fastembed

```bash
pip3 install langchain langchain_community streamlit streamlit_chat chromadb pypdf fastembed
```
### Set up Ollama
We need a LLM server which we can easily setup locally and do not have to worry about API keys!

To do this, download Ollama from https://ollama.com/
Ollama can be setup locally and provides multiple models: https://ollama.com/library

We can run a compact model - Mistral-7B

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
### Step 1: Initiatlize Mistral model 
Update the __init__() method - initialize Mistral using this API
https://api.python.langchain.com/en/latest/chat_models/langchain_community.chat_models.ollama.ChatOllama.html

````
    self.model = ChatOllama(model="mistral")
````

### Step 2: Split the uploaded document into smaller chunks using [text splitters](https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/)
- Here, we are using the [RecursiveCharacterTextSplitter](https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/recursive_text_splitter/)

Add the following code in the method processDocument()

```` 
    self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    document_chunks = self.text_splitter.split_documents(docs)
````

### Step 3: Vectorize the document chunks using [FastEmeddings](https://github.com/qdrant/fastembed) and store in [Chroma](https://github.com/chroma-core/chroma)
````
    chroma_vector_store = Chroma.from_documents(documents=document_chunks, embedding=FastEmbedEmbeddings())
````

#### Step 4: Configure the Vector store [Retriever](https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/vectorstore/) for the type of search
````
    self.retriever = chroma_vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 10, ## return top 5 chunks
                "score_threshold": 0.50, ## with scores above this value
            },
        )
````

#### Step 4: Add a system prompt template using Langchain [Prompts](https://python.langchain.com/v0.1/docs/modules/model_io/prompts/) 
````
    self.prompt_from_template = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know. Answer only as per what is mentioned in the document. 
            Use three sentences
             maximum and keep the answer concise. [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )
````

#### Step 5: Build a langchain conversion chain using prompt template and model with an output parser using [LCEL](https://python.langchain.com/v0.1/docs/expression_language/get_started/)
````
    self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt_from_template
                      | self.model
                      | StrOutputParser())
````

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





