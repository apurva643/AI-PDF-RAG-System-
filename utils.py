import re


def get_relevant_sentences(question, chunks):

    keywords = re.findall(
        r"\w+",
        question.lower()
    )

    relevant = []

    for chunk in chunks:

        sentences = re.split(
            r"(?<=[.!?])\s+",
            chunk
        )

        for sentence in sentences:

            score = 0

            for word in keywords:

                if word in sentence.lower():

                    score += 1

            if score > 0:

                relevant.append(sentence.strip())

    return relevant[:5]