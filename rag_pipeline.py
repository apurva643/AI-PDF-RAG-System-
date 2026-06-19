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

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text

        # Group citations by PDF
        citation_dict = {}

        for source in sources:

            pdf = source["pdf"]

            page = source["page"]

            if pdf not in citation_dict:

                citation_dict[pdf] = set()

            citation_dict[pdf].add(page)

        # Create clean source strings
        formatted_sources = []

        for pdf, pages in citation_dict.items():

            pages = sorted(
                list(pages)
            )

            page_string = ",".join(

                str(page)

                for page in pages

            )

            formatted_sources.append(

                f"{pdf} (pages {page_string})"

            )

        return {

            "answer": answer,

            "sources": formatted_sources

        }

    except Exception as e:

        print(e)

        return str(e)