def chunk_text(
    pages,
    chunk_size=500,
    overlap=100
):

    all_chunks = []

    for page_data in pages:

        text = page_data["text"]

        page_number = page_data["page"]

        for i in range(
            0,
            len(text),
            chunk_size-overlap
        ):

            chunk = text[
                i:i+chunk_size
            ]

            all_chunks.append(

                {
                    "text": chunk,
                    "page": page_number
                }

            )

    return all_chunks