
from utils import get_relevant_sentences
from embeddings import get_embeddings
from memory import (
    conversation_history,
    current_topic
)
from vector_store import retrieve_chunks
from google import genai
from config import GEMINI_API_KEY
from keyword_search import (
    keyword_search
)
import time

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

    follow_up_words = [

        "example",

        "advantages",

        "disadvantages",

        "uses",

        "applications",

        "where",

        "why",

        "how",

        "difference",

        "types",

        "benefits",

        "drawbacks",

        "explain it",

        "tell me more",

        "its"

    ]

    question_lower = question.lower()

    is_followup = any(

        word in question_lower

        for word in follow_up_words

        )

    if is_followup:

        search_query = (

            current_topic["topic"]

            + " "

            + question

        )

    else:

        search_query = question
    question_embedding = get_embeddings(

        [search_query]

    )[0]
    print("Search Query:", search_query)
    print("Current Topic:", current_topic["topic"])
    print("Is Followup:", is_followup)

    # Retrieve top chunks and sources
    retrieved_chunks, sources, distances = retrieve_chunks(
        question_embedding
    )
    keyword_chunks = keyword_search(
    search_query
    )
    print(
        "Keyword chunks:"
    )

    for chunk in keyword_chunks:

        print(
            chunk[:150]
        )


    retrieved_chunks.extend(
        keyword_chunks
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

    Format your answer using bullet points whenever appropriate.

    If the answer contains steps,
    number them.

    If the answer is a definition,
    give the definition first,
    then explain it in 2–4 bullet points.

    Do not mention the retrieved context or sources in your answer.

    Current Topic:

    {topic}

    Conversation History:

    {history}

    Context:

    {context}

    Question:

    {question}
    """

    response = None

    for attempt in range(3):

        try:

            response = client.models.generate_content(

                model="gemini-2.5-flash",

                contents=prompt

            )

            break

        except Exception as e:

            print(

                f"Attempt {attempt + 1} failed:",

                e

            )

            time.sleep(5)

    if response is None:

        return {

            "answer":

            "The AI service is temporarily busy. Please try again in a few seconds.",

            "confidence":

            "Unavailable",

            "sources": []

        }

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

    if not is_followup:

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
    relevant_sentences = get_relevant_sentences(

        question,

        retrieved_chunks

    )

    return {

        "answer": answer,

        "confidence": confidence,

        "sources": formatted_sources,

        "supporting_sentences": relevant_sentences

    }

    