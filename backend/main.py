from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import sys
sys.path.append('..')  # for import of rag_logic etc.

from rag_logic import retrieve_relevant_chunks
import openai
import os

app = FastAPI()

# Allow CORS for local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    project_context: str = ""
    history: List[dict] = []

from pydantic import BaseModel, Field

class ChatResponse(BaseModel):
    reply: str
    sources: list = Field(default_factory=list)
    response_time: float = 0.0
    tokens: int = 0
    cost: float = 0.0
    source_type: str = ""
    source_title: str = ""

    class Config:
        orm_mode = True

@app.post("/api/chat", response_model=ChatResponse, response_model_exclude_none=False)
async def chat_endpoint(req: ChatRequest):
    import time
    query = req.message
    relevant_chunks = retrieve_relevant_chunks(query)
    relevant_segments_text = ""
    sources = []
    source_type = None
    source_title = None
    if relevant_chunks:
        for i, chunk in enumerate(relevant_chunks):
            content = chunk.get('content', None)
            url = chunk.get('url', None)
            typ = chunk.get('type', None)
            title = chunk.get('title', None)
            if content is not None:
                relevant_segments_text += f"\n\nSegment {i+1}: {content}"
                if url:
                    relevant_segments_text += f"\n[Source]({url})"
                    sources.append(url)
                    if typ and not source_type:
                        source_type = typ
                    if title and not source_title:
                        source_title = title
    else:
        relevant_segments_text = "No direct YC content found for this specific query."
    from chatbot_app import generate_mentor_zero_response
    # --- Timing and token usage ---
    t0 = time.time()
    response, usage = generate_mentor_zero_response(req.history + [{"role": "user", "content": query}], req.project_context, relevant_segments_text, return_usage=True)
    t1 = time.time()
    response_time = round(t1 - t0, 2)
    tokens = None
    cost = None
    if usage:
        tokens = usage.get("total_tokens", 0)
        # Example cost calc: $0.002 per 1K tokens for gpt-3.5-turbo
        cost = round((tokens or 0) * 0.002 / 1000, 5)
    else:
        tokens = 0
        cost = 0.0
    return ChatResponse(
        reply=response,
        sources=sources,
        response_time=response_time if response_time is not None else 0.0,
        tokens=tokens,
        cost=cost,
        source_type=source_type if source_type is not None else "",
        source_title=source_title if source_title is not None else ""
    )

@app.post("/api/refresh")
async def refresh_endpoint():
    # Call your data refresh script
    import subprocess
    result = subprocess.run(['bash', 'update_yc_data.sh'], capture_output=True, text=True)
    return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
