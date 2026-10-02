from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.retrieval_service import search_documnets
from services.generation_service import generate_answer

from fastapi.responses import StreamingResponse
from fastapi import HTTPException


app = FastAPI(title="Campus AI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    query: str


@app.get("/")
def root():
    return {"RESPONCE": "WELCOME TO HOME PAGE"}


@app.post("/chat")
def chat(request: ChatRequest):

    try:
        result = search_documnets(request.query)

        retrived_documents = result["documents"][0]
        retrieved_metadata = result["metadatas"][0]

        sources = list(
            {
                (metadata["source"], metadata["page"]): {
                    "file": metadata["source"],
                    "page": metadata["page"],
                }
                for metadata in retrieved_metadata
            }.values()
        )

        def generate_stream():
            for chunk in generate_answer(
                request.query, retrived_documents, retrieved_metadata
            ):
                yield chunk

        return StreamingResponse(generate_stream(), media_type="text/plain")
    except Exception as error:
        print(f"Chat Error:{error}")

        raise HTTPException(
            status_code=500, detail="CampusAI was unable to process the request"
        )
