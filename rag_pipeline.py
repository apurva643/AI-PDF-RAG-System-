from embeddings import get_embeddings
from vector_store import retrieve_chunks

from google import genai
from config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def ask_question(question):

    # Convert question to vector
    question_embedding = get_embeddings(
        [question]
    )[0]

    # Retrieve top chunks and sources
    retrieved_chunks, sources = retrieve_chunks(
        question_embedding
    )

    # Handle no retrieved chunks
    if len(retrieved_chunks) == 0:

        return (
            "I couldn't find the answer "
            "in the uploaded PDF."
        )

    # Convert chunks into context
    context = "\n".join(
        retrieved_chunks
    )

    # Create prompt
    prompt = f"""
You are a helpful assistant.

Answer ONLY using the provided context.

If the answer is not available in the context, say:

"I couldn't find the answer in the uploaded PDF."

Provide concise answers.

Context:

{context}

Question:

{question}
"""

    # Gemini call
    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text

        unique_sources = []

        for source in sources:

            if source not in unique_sources:

             unique_sources.append(
               source
             )

        return {

            "answer": answer,

            "sources": unique_sources

        }

    except Exception as e:

        print(e)

        return str(e)