from rank_bm25 import BM25Okapi
import re

bm25 = None

all_chunks = []


def build_keyword_index(chunks):

    global bm25
    global all_chunks

    all_chunks.extend(

        [

            chunk["text"]

            for chunk in chunks

        ]

    )

    print(

        "Total chunks indexed:",

        len(all_chunks)

    )

    tokenized_chunks = [

        re.findall(

            r"\w+",

            chunk.lower()

        )

        for chunk in all_chunks

    ]

    bm25 = BM25Okapi(

        tokenized_chunks

    )


def keyword_search(

    question,

    top_k=3

):

    global bm25

    if bm25 is None:

        return []

    tokenized_question = re.findall(

        r"\w+",

        question.lower()

    )

    scores = bm25.get_scores(

        tokenized_question

    )

    ranked_indices = sorted(

        range(

            len(scores)

        ),

        key=lambda i: scores[i],

        reverse=True

    )

    return [

        all_chunks[i]

        for i in ranked_indices[:top_k]

    ]