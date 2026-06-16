import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="pdf_collection",
    metadata={
        "hnsw:space": "cosine"
    }
)


def store_chunks(chunks, embeddings):

    ids = []

    for i in range(len(chunks)):

        ids.append(str(i))


    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=ids
    )


def retrieve_chunks(question_embedding):

    results = collection.query(
        query_embeddings=[
            question_embedding.tolist()
        ],
        n_results=3
    )

    if len(results["documents"][0]) == 0:

        return []

    return results["documents"][0]