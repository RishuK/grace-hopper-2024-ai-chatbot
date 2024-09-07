from typing import List
from langchain_community.graphs import Neo4jGraph
from langchain.docstore.document import Document
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.text_splitter import TokenTextSplitter
from langchain_community.vectorstores import Neo4jVector
from langchain.chains import RetrievalQA
import gradio as gr
import os
from neo4j import GraphDatabase
from yfiles_jupyter_graphs import GraphWidget
from langchain_core.prompts import PromptTemplate

os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "Password" # replace with password value

graph = Neo4jGraph()


text = """Emily is an employee at TechNova, a leading technology company based in Silicon Heights. She has been working there for the past four years as a software developer. James is also an employee at TechNova, where he works as a data analyst. He joined the company three years ago after completing his undergraduate studies. TechNova is a renowned technology company that specializes in developing innovative software solutions and advanced artificial intelligence systems. The company boasts a diverse team of talented professionals from various fields. Both Emily and James are highly skilled experts who contribute significantly to TechNova's achievements. They collaborate closely with their respective teams to create cutting-edge products and services that cater to the dynamic needs of the company's clients."""

# Initialize TokenTextSplitter with desired parameters
text_splitter = TokenTextSplitter(
    chunk_size=100,  # Adjust chunk size as needed
    chunk_overlap=20  # Adjust overlap to maintain context
)

# Convert the formatted text into a list of Document objects
documents = [Document(page_content=text)]

# Split the text into chunks
texts = text_splitter.split_documents(documents)

# Print the split chunks
for i, chunk in enumerate(texts):
    print(f"Chunk {i+1}:\n{chunk}\n")

llm = Ollama(model="llama3")

llm_transformer = LLMGraphTransformer(
    llm=llm, 
    allowed_nodes=["Author", "Book", "Publisher"],
    allowed_relationships=["WRITTEN_BY", "PUBLISHED_BY"],
)

# Extract graph data
graph_documents = llm_transformer.convert_to_graph_documents(texts)
print("graph documents", graph_documents)

print(f"Nodes:{graph_documents[0].nodes}") # this is to see Nodes of generated graph
print("-----------------------------------------------------------------")
print(f"Relationships:{graph_documents[0].relationships}") 



# directly show the graph resulting from the given Cypher query
default_cypher = "MATCH (s)-[r:!MENTIONS]->(t) RETURN s,r,t LIMIT 50"

def showGraph(cypher: str = default_cypher):
    # create a neo4j session to run queries
    driver = GraphDatabase.driver(
        uri = os.environ["NEO4J_URI"],
        auth = (os.environ["NEO4J_USERNAME"],
                os.environ["NEO4J_PASSWORD"]))
    session = driver.session()
    widget = GraphWidget(graph = session.run(cypher).graph())
    widget.node_label_mapping = 'id'
    #display(widget)
    return widget

showGraph()


# Store to neo4j
graph.add_graph_documents(
    graph_documents,
    baseEntityLabel=True,
    include_source=True
)
print("Documents successfully added to Graph DataBase")


#load the embedding model
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name  = "BAAI/bge-base-en-v1.5")


vector_index = Neo4jVector.from_existing_graph(
    embeddings,
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding"
)

qa_chain = RetrievalQA.from_chain_type(
    llm, retriever=vector_index.as_retriever()
)

print(qa_chain.combine_documents_chain.llm_chain.prompt.template)

# Passing custom prompt template
template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use three sentences maximum and keep the answer as concise as possible. 
Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

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
interface = gr.Interface(
    fn=query_document_details,        # Function to call
    inputs=gr.Textbox(label="Enter your question"),  # Input textbox
    outputs=gr.Textbox(label="Answer")   # Output textbox
)

# Launch the interface
interface.launch()