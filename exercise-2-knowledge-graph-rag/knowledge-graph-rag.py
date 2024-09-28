from langchain_community.graphs import Neo4jGraph
from langchain.docstore.document import Document
from langchain_community.llms import Ollama
from langchain_community.vectorstores.utils import filter_complex_metadata
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.text_splitter import TokenTextSplitter
from langchain_community.vectorstores import Neo4jVector
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
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

    # Initialize TokenTextSplitter with desired parameters
    # Read more about it here: https://api.python.langchain.com/en/latest/base/langchain_text_splitters.base.TokenTextSplitter.html 
    # TokenTextSplitter breaks down text into smaller chunks for easier processing and retrieval.
    # It splits a raw text string by first converting the text into tokens, then splits these tokens into chunks and converts the tokens within a single chunk back into text.
    # Adjust chunk_size and chunk_overlap according to your needs.
    # The chunk size should be at least as large as the average length of your queries.
    # The chunk overlap should be smaller than the chunk size to maintain context.
    text_splitter = TokenTextSplitter(
        chunk_size=200,  # Adjust chunk size as needed
        chunk_overlap=20  # Adjust overlap to maintain context
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

# Using Ollama to locally run large language models. 
# https://api.python.langchain.com/en/latest/llms/langchain_community.llms.ollama.Ollama.html
llm = Ollama(model="llama3")

# LLMGraphTransformer converts textual documents into graph-based documents using LLM.
# https://api.python.langchain.com/en/latest/graph_transformers/langchain_experimental.graph_transformers.llm.LLMGraphTransformer.html
llm_transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Company", "Person", "Supplier", "Warehouse", "Store", "Product", "Shipment", "Customer", "External Factor"], # Specifies which node types are allowed in the graph. Defaults to an empty list, allowing all node types.
    allowed_relationships=["WORKS_AT", "CREATES", "SUPPLIES", "STOCKS", "DELIVERS_TO", "LOCATED_AT", "AFFECTS", "MANAGES", "CONTAINS", "HAS_CONTRACT_WITH", "HAS_INVENTORY", "INFLUENCES" ], # Specifies which relationship types are allowed in the graph. Defaults to an empty list, allowing all relationship types.
)

## Filter out any complex data or metadata types that are not supported for a vector store, before we pass it for vertorization
# https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.utils.filter_complex_metadata.html
document_chunks = filter_complex_metadata(documents)


# Extract graph data by converting a sequence of documents into graph documents.
# https://api.python.langchain.com/en/latest/graph_transformers/langchain_experimental.graph_transformers.llm.LLMGraphTransformer.html#langchain_experimental.graph_transformers.llm.LLMGraphTransformer.convert_to_graph_documents
graph_documents = llm_transformer.convert_to_graph_documents(documents)
print("graph documents", graph_documents)

# Print the nodes and relationships of the generated graph 
print(f"Nodes:{graph_documents[0].nodes}") 
print("-----------------------------------------------------------------")
print(f"Relationships:{graph_documents[0].relationships}")

# Store to neo4j
# This method constructs nodes and relationships in the graph based on the provided GraphDocument objects.
# https://api.python.langchain.com/en/latest/graphs/langchain_community.graphs.neo4j_graph.Neo4jGraph.html#langchain_community.graphs.neo4j_graph.Neo4jGraph.add_graph_documents
graph.add_graph_documents(
    graph_documents,
    baseEntityLabel=True,
    include_source=True
)
print("Documents successfully added to Graph DataBase")

# Load the HuggingFace sentence_transformers embedding models.
# https://api.python.langchain.com/en/latest/embeddings/langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings.html
# https://huggingface.co/BAAI/bge-base-en-v1.5
embeddings = HuggingFaceEmbeddings(model_name  = "BAAI/bge-base-en-v1.5")

# Initialize and return a Neo4jVector instance from existing graph.
# This method initializes and returns a Neo4jVector instance using the provided parameters and the existing graph. 
# It validates the existence of the indices and creates new ones if they don’t exist.
# https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.neo4j_vector.Neo4jVector.html#langchain_community.vectorstores.neo4j_vector.Neo4jVector.from_existing_graph
vector_index = Neo4jVector.from_existing_graph(
    embeddings,
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding"
)

# Create a RetrievalQA chain using the Neo4jVector as the retriever.
qa_chain = RetrievalQA.from_chain_type(
    llm, retriever=vector_index.as_retriever()
)

# See the default prompt template used for the retrieval qa chain
print(qa_chain.combine_documents_chain.llm_chain.prompt.template)

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
