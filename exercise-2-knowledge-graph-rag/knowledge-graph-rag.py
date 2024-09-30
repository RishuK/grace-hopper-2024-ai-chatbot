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
os.environ["NEO4J_PASSWORD"] = "Password" # replace with the password value here

# Neo4j database wrapper for performing the graph operations.
# Read more about it here: https://api.python.langchain.com/en/latest/graphs/langchain_community.graphs.neo4j_graph.Neo4jGraph.html
graph = Neo4jGraph()

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

# LLMGraphTransformer converts textual documents into graph-based documents using LLM.
# https://api.python.langchain.com/en/latest/graph_transformers/langchain_experimental.graph_transformers.llm.LLMGraphTransformer.html
llm_transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Company", "Person", "Product", "Supplier", "Warehouse", "Store", "Shipment", "Customer", "External Factor", "Supply Chain", "Location", "Weather Condition", "Holiday", "Region", "Sales Trend"], # Specifies which node types are allowed in the graph. Defaults to an empty list, allowing all node types.
    allowed_relationships=["WORKS_FOR", "CREATES", "SUPPLIES", "STOCKS", "DELIVERS_TO", "LOCATED_AT", "AFFECTED_BY", "AFFECTS", "MANAGES", "CONTAINS", "HAS_CONTRACT_WITH", "HAS_INVENTORY", "INFLUENCES" ], # Specifies which relationship types are allowed in the graph. Defaults to an empty list, allowing all relationship types.
)

# Extract graph data by converting a sequence of documents into graph documents.
# https://api.python.langchain.com/en/latest/graph_transformers/langchain_experimental.graph_transformers.llm.LLMGraphTransformer.html#langchain_experimental.graph_transformers.llm.LLMGraphTransformer.convert_to_graph_documents
graph_documents = llm_transformer.convert_to_graph_documents(documents)
print("graph documents", graph_documents)

# Print the nodes and relationships of the generated graph 
print(f"Nodes:{graph_documents[0].nodes}") 
print("-----------------------------------------------------------------")
print(f"Relationships:{graph_documents[0].relationships}")

# Print all the nodes and relationships of the generated graph 
for graph_doc in graph_documents:
    print("\nNodes:")
    for node in graph_doc.nodes:
        print(f"Id: {node.id}, Type: {node.type}")
    print("\nRelationships:")
    for relationship in graph_doc.relationships:
        print(f"Source: {relationship.source}, Target: {relationship.target}, Type: {relationship.type}")

# Store to neo4j
# This method constructs nodes and relationships in the graph based on the provided GraphDocument objects.
# https://api.python.langchain.com/en/latest/graphs/langchain_community.graphs.neo4j_graph.Neo4jGraph.html#langchain_community.graphs.neo4j_graph.Neo4jGraph.add_graph_documents
graph.add_graph_documents(
    graph_documents,
    baseEntityLabel=True,
    include_source=True
)
print("Documents successfully added to Graph DataBase")

# Instantiate the Ollama embedding model and generate embeddings using the locally running LLaMA3.1-8b
# https://python.langchain.com/api_reference/ollama/embeddings/langchain_ollama.embeddings.OllamaEmbeddings.html 
local_embeddings = OllamaEmbeddings(model="llama3.1:8b")

# Initialize and return a Neo4jVector instance from existing graph.
# This method initializes and returns a Neo4jVector instance using the provided parameters and the existing graph. 
# It validates the existence of the indices and creates new ones if they don’t exist.
# https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.neo4j_vector.Neo4jVector.html#langchain_community.vectorstores.neo4j_vector.Neo4jVector.from_existing_graph
vector_index = Neo4jVector.from_existing_graph(
    embedding=local_embeddings,
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding"
)

# Create a RetrievalQA chain using the Neo4jVector as the retriever.
qa_chain = RetrievalQA.from_chain_type(
    llm, retriever=vector_index.as_retriever()
)

# Creating custom prompt template
# A prompt template consists of a string template.
# It accepts a set of parameters that can be used to generate a prompt for a language model.
template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use three sentences maximum and keep the answer as concise as possible. 
Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""

# Create a PromptTemplate instance with the custom prompt template for the language model.
# https://api.python.langchain.com/en/latest/prompts/langchain_core.prompts.prompt.PromptTemplate.html
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

# Create a RetrievalQA Chain for question-answering against an index using the Neo4jVector as the retriever. 
# https://api.python.langchain.com/en/latest/chains/langchain.chains.retrieval_qa.base.RetrievalQA.html#
# Todo: Replace it with create_retrieval_chain()
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vector_index.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

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
