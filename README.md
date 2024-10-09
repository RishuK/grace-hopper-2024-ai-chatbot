# AI Chatbot Masterclass: Building LLM-Powered RAG Chatbots with LangChain & Knowledge Graphs

Welcome to the Grace Hopper workshop 2024!

Are you curious about the buzz around Generative AI and do not know how to get involved?
This one hour workshop is your step towards that direction where you will learn basic concepts of GenAI, Retrieval Augmented Generation (RAG), Large Language Models (LLMs), Knowledge Graphs, LangChain, Prompt Engineering, and more. All these concepts will be covered using a real-world use case with sample dataset and code modules.
At the end of the workshop, you will have a working AI-powered chatbot, which will understand your questions and answer them. This chatbot can be easily extended to any other use cases. You'll walk away with practical GenAI knowledge, hands-on experience, and the confidence to apply these skills to future projects.

Link to the GHC 2024 Workshop Session: [GHC Workshop Link](https://ghc.anitab.org/session-catalog/?search.sessiontype=1712687033982003Uicv&search.sessiontracks=1715091731850001IqQr&search.experiencetype=option_1713202494133#/session/1717218930814001YQKl)

# Option 1 - set up your local IDE with python, dependencies and clone the repo
## Pre-requisites Workspace setup starts here

### Steps:

#### Step 1: Install python3 (and pip3)

##### python version: 3.12.5

https://www.python.org/downloads/macos/

- Download and use the installer
- pip3 should get auto-installed with python. 

#### Step 2: Clone the repository
````
git clone https://github.com/RishuK/grace-hopper-2024-ai-chatbot.git
````

#### Step 3: Go to each excercise folder and **execute the pre-requisites under each folder below**

- excercise-1-chatbot-rag-pdf
- excercise-2-knowledge-graph-rag

## ---Pre-requisites Workspace setup ends here---

# Option 2 - Each example has a Jupyter notebook code which can be imported into your locally running Jupyter notebook setup


### Workshop Execution Overview

These workshop contains the following branches:

1. Master - contains the target state of the workshop exercises, which can you directly execute
2. exercises - contains step-wise code-writing exercises

Steps:

1. Checkout branch 'exercises'
````
git checkout exercises
````

2. We will work through the following exercises. Each exercise has its README file that will guide you step by step

#### Exercise 1 : Building RAG Chatbot using vector store
[Exercise-1 Readme](./exercise-1-chatbot-rag-pdf/README.md)

#### Exercise 2: RAG Chatbot with Knowledge Graph

[Exercise-2 Readme](./exercise-2-knowledge-graph-rag/README.md)

- [Neo4j Desktop Installation and Setup Steps](./exercise-2-knowledge-graph-rag/README.md/#neo4j-desktop-setup)
- [Sample Data Description for Knowledge Graph Exercise](./exercise-2-knowledge-graph-rag/README.md/#sample-data-file-description-for-the-knowledge-graph)
