import os
import tempfile
import streamlit as st
from streamlit_chat import message
from rag_pipeline import ChatDocument

st.set_page_config(page_title="ChatDocument")

def show_chatbot_questions_answers():
    st.subheader("Ask your questions here: ")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_question():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        with st.session_state["thinking_spinner"], st.spinner(f"Finding answers"):
            agent_text = st.session_state["assistant"].chatQuestion(user_text)

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))


def read_and_process_document():
    st.session_state["assistant"].clear()
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["assistant"].processDocument(file_path)
        os.remove(file_path)


def chat_bot_page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = ChatDocument()

    st.header("LLM-powerd RAG Chatbot with Langchain")

    st.subheader("Upload your document to kick-off the chatbot")
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_process_document,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    st.session_state["ingestion_spinner"] = st.empty()

    show_chatbot_questions_answers()
    st.text_input("Question", key="user_input", on_change=process_question)


if __name__ == "__main__":
    chat_bot_page()