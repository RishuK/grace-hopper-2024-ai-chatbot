from langchain_community.graphs import Neo4jGraph
from langchain.docstore.document import Document
from langchain_community.chat_models import ChatOllama
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Neo4jVector
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
import gradio as gr
import os

# Refer to the Neo4j Desktop Installation & Setup Steps in the Readme. 
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "Password" # Replace with your neo4j password value here

## Step-1: Create Neo4j database wrapper for performing the graph operations.
## Add step-1 code here. 

# Specify the path to your text file
file_path = "Lumina.txt"

try:
    # Read the text from the file
    with open(file_path, "r", encoding='utf-8') as file:
        text = file.read()

    # Initialize RecursiveCharacterTextSplitter with desired parameters
    # Read more about it here: https://sj-langchain.readthedocs.io/en/latest/text_splitter/langchain.text_splitter.RecursiveCharacterTextSplitter.html 
    # RecursiveCharacterTextSplitter recursively breaks down text into smaller chunks for easier processing and retrieval.
    # This is the recommended text splitter for generic text. 
    # It is parameterized by a list of characters, the default list is ["\n\n", "\n", " ", ""]. It tries to split on them in order until the chunks are small enough. 
    # This has the effect of trying to keep all paragraphs (and then sentences, and then words) together as long as possible, as those would generically seem to be the strongest semantically related pieces of text.
    # Adjust chunk_size and chunk_overlap according to your needs.
    # The chunk size should be at least as large as the average length of your queries.
    # The chunk overlap should be smaller than the chunk size to maintain context.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,  # Adjust chunk size as needed
        chunk_overlap=24  # Adjust overlap to maintain context
    )

    # Convert the formatted text into a list of Document objects
    texts = []

    # Docstores are classes to store and load Documents.
    # The Docstore is a simplified version of the Document Loader.
    # https://python.langchain.com/v0.2/api_reference/community/docstore.html
    document = Document(page_content=text)
    texts.append(document)

    # Split the text into chunks
    documents = text_splitter.split_documents(texts)
    # Print the split chunks
    for i, chunk in enumerate(documents):
        print(f"Chunk {i+1}:\n{chunk}\n")

# Print an error message if the file is not found.
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")

# Instantiating our model object with relevant params for Chat Completion. 
# Running LLaMA3.1-8b LLM locally using Ollama.
# https://api.python.langchain.com/en/latest/chat_models/langchain_community.chat_models.ollama.ChatOllama.html
llm = ChatOllama(
    model="llama3.1:8b", # LLM Model running locally using Ollama
    temperature=0.1, # Temperature parameter for LLM model, ranges from 0 to 1, controls the randomness of the output.
)

## Step-2: Convert textual documents into graph-based documents using LLMGraphTransformer
## Add step-2 code here and uncomment the below print lines to see the generated graph details.


# # Print the nodes and relationships of the generated graph 
# print(f"Nodes:{graph_documents[0].nodes}") 
# print("-----------------------------------------------------------------")
# print(f"Relationships:{graph_documents[0].relationships}")

# # Print all the nodes and relationships of the generated graph 
# for graph_doc in graph_documents:
#     print("\nNodes:")
#     for node in graph_doc.nodes:
#         print(f"Id: {node.id}, Type: {node.type}")
#     print("\nRelationships:")
#     for relationship in graph_doc.relationships:
#         print(f"Source: {relationship.source}, Target: {relationship.target}, Type: {relationship.type}")

## Step-3: Store to neo4j
## Add step-3 code here. 

## Step-4: Initialize and return a Neo4jVector instance from existing graph using OllamaEmbeddings.
## Add step-4 code here.

## Step-5: Create a RetrievalQA chain using custom prompt template and the Neo4jVector as the retriever.
## Add step-5 code here. 

# Define the function for querying document details
def query_document_details(query):
    if query is None:
        return "Error: Query cannot be None"
    try:
        result = qa_chain({"query": query})
        return result["result"]
    except Exception as e:
        return f"Error: {str(e)}"

# Create a Gradio interface
# https://www.gradio.app/guides/the-interface-class
interface = gr.Interface(
    fn=query_document_details,        # Function to call
    inputs=gr.Textbox(label="Enter your question"),  # Input textbox as Gradio component to be used for the input
    outputs=gr.Textbox(label="Answer")   # Output textbox as Gradio component to be used for the output
)

# Launch the interface
interface.launch()