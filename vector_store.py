import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="pdf_collection",
    metadata={
        "hnsw:space": "cosine"
    }
)


def store_chunks(
    chunks,
    embeddings,
    source
):

    ids = [

        source + "_" + str(i)

        for i in range(
            len(chunks)
        )

    ]

    collection.add(

        documents=chunks,

        embeddings=embeddings.tolist(),

        ids=ids,

        metadatas=[

            {

                "source": source

            }

            for _ in chunks

        ]

    )


def retrieve_chunks(question_embedding):

    results = collection.query(

        query_embeddings=[
            question_embedding.tolist()
        ],

        n_results=10,

        include=[
            "documents",
            "metadatas"
        ]

    )

    if len(results["documents"][0]) == 0:

        return [], []

    documents = results["documents"][0]

    sources = [

        metadata["source"]

        for metadata in

        results["metadatas"][0]

    ]

    return documents, sources