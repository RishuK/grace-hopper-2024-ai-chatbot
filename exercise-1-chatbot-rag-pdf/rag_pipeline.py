from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.schema.output_parser import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.utils import filter_complex_metadata

class ChatDocument:
    vector_store = None
    retriever = None
    chain = None

    def __init__(self):

        ## Step 1: Initialize Mistral model
        ## Add step 1 code here and remove 'pass'

        pass

    ## processDocument() method called from chat_ui.py
    def processDocument(self, pdf_file_path: str):
        ## Accepts a filepath
        docs = PyPDFLoader(file_path=pdf_file_path).load()

        ## Step 2: Initialize the text splitter to split the uploaded document into smaller chunks
        ## Add step 2 code here

        ## Filter out any complex data not supported by Chroma DB, before we pass it for vertorization
        ## Please Comment out the following code
        ## document_chunks = filter_complex_metadata(document_chunks)
        ## print(document_chunks)

        ## Step 3: Vectorize the document chunks using FastEmeddings and store in ChromaDB
        ## Add step 3 code here

        ## Step 4: Configures the Vector store Retriever class for the type of search
        ## Add step 4 code here

        ## Step 5: Add a system prompt template using Langchain Prompts
        ## Add step 5 code here

        ## Step 6: Build a chain of prompt template and model with an output parser using LCEL
        ## Add step 6 code here


    def chatQuestion(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."

        print(query)

        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
