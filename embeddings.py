from sentence_transformers import SentenceTransformer

model = None


def get_embeddings(chunks):

    global model

    if model is None:

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    embeddings = model.encode(
        chunks
    )

    return embeddings