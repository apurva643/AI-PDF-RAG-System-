from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from pdf_parser import extract_text_from_pdf
from chunking import chunk_text
from embeddings import get_embeddings
from vector_store import store_chunks
from rag_pipeline import ask_question


app = FastAPI()


class QuestionRequest(BaseModel):

    question: str


@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    contents = await file.read()

    text = extract_text_from_pdf(
        contents
    )

    if len(text) == 0:

        return {

          "message":
          "No text found in PDF"

        }
    chunks = chunk_text(
        text
    )

    embeddings = get_embeddings(

    [

        chunk["text"]

        for chunk in chunks

    ]

)

    store_chunks(
    chunks,
    embeddings,
    file.filename
    )

    return {
        "message":
        "PDF uploaded successfully"
    }


@app.post("/ask")
def ask(
    data: QuestionRequest
):

    response = ask_question(
        data.question
    )

    return response
    