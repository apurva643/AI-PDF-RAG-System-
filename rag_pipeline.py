from embeddings import get_embeddings
from memory import (
    conversation_history,
    current_topic
)
from vector_store import retrieve_chunks

from google import genai
from config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def ask_question(question):
    print(

        "Search Query:",

        current_topic["topic"]

        + " "

        + question

    )
    # Convert question to vector
    search_query = (

        current_topic["topic"]

        + " "

        + question

    )

    question_embedding = get_embeddings(

        [search_query]

    )[0]

    # Retrieve top chunks and sources
    retrieved_chunks, sources, distances = retrieve_chunks(
        question_embedding
    )
    unique_chunks = []

    for chunk in retrieved_chunks:

        is_duplicate = False

        chunk_words = set(

            chunk.lower().split()

        )

        for existing_chunk in unique_chunks:

            existing_words = set(

              existing_chunk.lower().split()

            )

            common_words = len(

                chunk_words.intersection(

                    existing_words

                )

            )

            if common_words > 80:

                is_duplicate = True

                break

        if not is_duplicate:

            unique_chunks.append(

                chunk

            )

    retrieved_chunks = unique_chunks
    MAX_CONTEXT_CHUNKS = 3

    retrieved_chunks = retrieved_chunks[
    :MAX_CONTEXT_CHUNKS
    ]

    sources = sources[
    :MAX_CONTEXT_CHUNKS
    ]

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
    history = "\n".join(
    conversation_history
    )
    topic = current_topic["topic"]

    # Create prompt
    prompt = f"""
    You are a helpful assistant.

    Answer ONLY using the provided context.

    If the answer is not available in the context, say:

    "I couldn't find the answer in the uploaded PDF."

    Use conversation history and the current topic to understand follow-up questions.

    If the user asks for an example, provide a practical example whenever possible.

    If the user asks follow-up questions such as:

    "Explain it simply"

    "Give one example"

    "Where is it used"

    "What are its advantages"

    infer the topic from the conversation history and current topic.

    Keep answers concise but complete.

    Current Topic:

    {topic}

    Conversation History:

    {history}

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
        best_distance = min(
            distances
        )   

        if best_distance < 0.4:

            confidence = "High"

        elif best_distance < 0.7:

            confidence = "Medium"

        else:

            confidence = "Low"

        if len(question) > 5:

            current_topic["topic"] = question
        conversation_history.append(

            "User: " + question

        )
        conversation_history.append(

            "Assistant: " + answer

        )
        if len(conversation_history) > 10:

            conversation_history.pop(0)

            conversation_history.pop(0)

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

            "confidence": confidence,

            "sources": formatted_sources,

            "retrieved_chunks": retrieved_chunks

        }
    except Exception as e:

        print(e)

        return str(e)