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

        ## Instantiating our model object with relevant params for Chat Completion.
        ## Running Mistral LLM locally using Ollama.
        ## https://api.python.langchain.com/en/latest/chat_models/langchain_community.chat_models.ollama.ChatOllama.html
        self.model = ChatOllama(model="mistral")

    ## processDocument() method called from chat_ui.py
    def processDocument(self, pdf_file_path: str):
        ## Accepts a filepath
        docs = PyPDFLoader(file_path=pdf_file_path).load()

        ## Different text splitters available - https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)

        ## Splits the document into smaller chunks
        ## https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/
        document_chunks = self.text_splitter.split_documents(docs)

        ## Filter out any complex data not supported by Chroma DB, before we pass it for vertorization
        document_chunks = filter_complex_metadata(document_chunks)
        print(document_chunks)

        ## Vectorize the document chunks using FastEmeddings and store in Chroma
        chroma_vector_store = Chroma.from_documents(documents=document_chunks, embedding=FastEmbedEmbeddings())

        ## Langchain retrievers: https://python.langchain.com/v0.1/docs/modules/data_connection/retrievers/vectorstore/
        ## Configures the Vector store Retriever class for the type of search
        self.retriever = chroma_vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 10, ## return top 5 chunks
                "score_threshold": 0.50, ## with scores above this value
            },
        )

        ## Prompt template for a language model.
        ## It consists of a string template, which can contain system prompt, human prompt and context.
        ## https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.prompt.PromptTemplate.html
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

        ## Construct langchain conversion chain using LCEL (LangChain Expression Language)
        ## https://python.langchain.com/v0.1/docs/expression_language/get_started/
        ## Build a chain using prompt + model + output parser using LCEL
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt_from_template
                      | self.model
                      | StrOutputParser())

    def chatQuestion(self, query: str):
        if not self.chain:
            return "Please, add a PDF document first."

        print(query)

        return self.chain.invoke(query)

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None