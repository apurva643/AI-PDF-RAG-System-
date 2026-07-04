import streamlit as st
import requests

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

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

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

# -----------------------------
# Ask Question
# -----------------------------

st.divider()

st.subheader("Ask a Question")

question = st.text_input(
    "Enter your question"
)

if st.button("Ask"):

    if question.strip() == "":

        st.warning(
            "Please enter a question."
        )

    else:

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

            st.subheader("Answer")

            st.write(
                result["answer"]
            )

            st.success(
                f"Confidence: {result['confidence']}"
            )

            st.info(
                f"Response Time: {result['response_time']}"
            )

            st.subheader("Sources")

            for source in result["sources"]:

                st.write(
                    "📄",
                    source
                )

            if result["supporting_sentences"]:

                with st.expander(
                    "Supporting Evidence"
                ):

                    for sentence in result["supporting_sentences"]:

                        st.write(
                            "•",
                            sentence
                        )

        else:

            st.error(
                "Failed to get response from API."
            )