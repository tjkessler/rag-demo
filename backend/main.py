from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import chromadb
from chromadb.config import Settings
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chroma_client = chromadb.Client(Settings())
collection = chroma_client.create_collection("rag-demo")

model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()


class IngestRequest(BaseModel):
    """
    Request model for ingesting documents into the database.

    Attributes
    ----------
    documents : List[str]
        A list of strings, where each string is the content of a document to be
        ingested.
    """

    documents: List[str]


class QueryRequest(BaseModel):
    """
    Request model for querying the database and generating an answer.

    Attributes
    ----------
    query : str
        The query string for which the answer is to be generated.
    max_length : int, optional
        The maximum length of the generated answer (default is 128).
    top_k : int, optional
        The number of top relevant documents to retrieve from the database
        (default is 3).
    """

    query: str
    max_length: int = 128
    top_k: int = 3


@app.post("/ingest")
def ingest_docs(req: IngestRequest) -> dict:
    """
    Ingests a list of documents into the Chroma DB collection.

    Parameters
    ----------
    req : IngestRequest
        The request object containing the list of documents to be ingested.

    Returns
    -------
    dict
        A dictionary containing the status of the ingestion and the count of
        documents ingested.
    """

    for doc in req.documents:
        collection.add(
            documents=[doc],
            metadatas=[{"source": "user"}],
            ids=[str(hash(doc))]
        )
    return {"status": "success", "count": len(req.documents)}


@app.post("/query")
def query_docs(req: QueryRequest) -> dict:
    """
    Queries the Chroma DB collection for relevant documents based on the input
    query and generates an answer using the GPT-2 model.

    Parameters
    ----------
    req : QueryRequest
        The request object containing the query string, maximum length for the
        generated answer, and the number of top relevant documents to retrieve.

    Returns
    -------
    dict
        A dictionary containing the generated answer and the list of relevant
        documents retrieved from the database.
    """

    results = collection.query(query_texts=[req.query], n_results=req.top_k)
    docs = [d for d in results["documents"][0]]
    context = "\n".join(docs)
    input_text = f"Context: {context}\nQuestion: {req.query}\nAnswer:"
    inputs = tokenizer.encode(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=req.max_length,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"answer": answer, "documents": docs}
