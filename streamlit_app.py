import streamlit as st
import requests

if "messages" not in st.session_state:

    st.session_state.messages = []

st.set_page_config(
    page_title="RAG PDF Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Intelligent RAG PDF Chatbot")

st.caption(
    "Upload PDFs and ask questions using Retrieval-Augmented Generation."
)

# -----------------------------
# Upload PDF
# -----------------------------

with st.sidebar:

    st.header("📂 PDF Manager")

    uploaded_file = st.file_uploader(

        "Upload PDF",

        type=["pdf"]

    )
    if len(st.session_state.messages) == 0:

        with st.chat_message("assistant"):

            st.write(

                "👋 Welcome! Upload a PDF and ask me anything about it."

            )
    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

if uploaded_file is not None:

    if st.button("Upload PDF"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )

        if response.status_code == 200:

            st.success(
                response.json()["message"]
            )

        else:

            st.error("Failed to upload PDF.")
        st.divider()

        pdf_response = requests.get(

            "http://127.0.0.1:8000/pdfs"

        )

        if pdf_response.status_code == 200:

            st.subheader("Uploaded PDFs")

            for pdf in pdf_response.json()["uploaded_pdfs"]:

                st.write("📄", pdf)

# -----------------------------
# Ask Question
# -----------------------------

st.divider()

question = st.chat_input(

    "Ask a question about the uploaded PDF"

)

if question:

    st.session_state.messages.append(

        {

            "role": "user",

            "content": question
        }
    )
    with st.spinner(
        "Generating answer..."
        ):

        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={
                "question": question
                }
        )

        if response.status_code == 200:

            result = response.json()

            st.session_state.messages.append(

                {

                    "role": "assistant",

                    "content": result["answer"],

                    "confidence": result["confidence"],

                    "response_time": result["response_time"],

                    "sources": result["sources"],

                    "supporting_sentences": result["supporting_sentences"]

                }

            )

        else:

            st.error(

            "Failed to get response from API."

        )
st.divider()

for message in st.session_state.messages:

    avatar = "👤"

    if message["role"] == "assistant":

        avatar = "🤖"

    with st.chat_message(

        message["role"],

        avatar=avatar

    ):

        st.write(message["content"])

        if message["role"] == "assistant":

            col1, col2 = st.columns(2)

            with col1:

                st.success(

                    f"Confidence: {message['confidence']}"

                )

            with col2:

                st.info(

                    f"⏱ {message['response_time']}"

                )

            if message["sources"]:

                st.subheader("Sources")

                for source in message["sources"]:

                    st.write("📄", source)

            if message["supporting_sentences"]:

                with st.expander(

                    "Supporting Evidence"

                ):

                    for sentence in message["supporting_sentences"]:

                        st.write("•", sentence)