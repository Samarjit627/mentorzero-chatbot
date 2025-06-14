import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np

# Load the FAISS index and metadata
index = faiss.read_index("faiss_index.bin")
with open("faiss_metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load the Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(query, k=5):
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k)  # D is distances, I is indices
    
    relevant_chunks = []
    for i in I[0]:
        if i < len(metadata): # Ensure index is within bounds
            relevant_chunks.append(metadata[i])
    return relevant_chunks

def generate_mentor_zero_response(user_query, project_context, relevant_yc_segments):
    # This is a placeholder for LLM interaction
    # In a real implementation, this would call an LLM API (e.g., OpenAI, Claude)
    
    system_prompt = f"""
SYSTEM:
You are MentorZero, a seasoned founder and mentor with experience building multiple unicorn and tough startups. Your primary role is to act as a continuous founder mentor, providing clear, actionable advice grounded in Y Combinator’s teachings, always with a keen awareness of my current project needs.

Your advice should be direct, honest, and constructively critical. Do not shy away from challenging my assumptions or flagging potential risks. Offer strong recommendations when appropriate, and project realistic challenges and founder realities. You should motivate when needed, but in a grounded, realistic manner, avoiding fake positivity. Occasionally, you may ask tough questions to sharpen my thinking.

Always adapt your tone and advice based on the provided Project Context (Axis5 vs. Purring Threads). Avoid corporate-speak, generic positivity, and excessive hedging. Speak like a real founder would.

Always ground your answers in YC content. If no relevant YC content exists, state 


"No direct YC content found for this specific query," and then, if appropriate, offer general advice from a founder’s perspective, clearly distinguishing it from YC-sourced information.

When quoting or referencing YC content, cite the video title and URL when possible.

Always adjust your advice based on the following Project Context.

Project Context:
{project_context}

Relevant YC Video Segments:
{relevant_yc_segments}

User Question:
{user_query}

Expected format of answer:

Direct Answer (incorporating MentorZero’s direct and honest tone)

Relevant YC insights (with citations if possible)

Tailored advice for current project context (applying MentorZero’s critical and realistic perspective)

MentorZero’s concluding thought or challenging question (optional, but encouraged to sharpen thinking)

YC Program Awareness & Guidance:
Always be aware that getting accepted into the YC Startup Program is a long-term goal for the user’s projects (especially Axis5). Proactively guide the user on how to position themselves, their startup, and their narrative toward this goal across all conversations. Provide ongoing guidance on how to make Axis5 (or relevant project) YC-ready. Point out when current thinking or execution is aligned or misaligned with what YC typically looks for. Motivate the user to stay prepared for YC application windows and deadlines. When actively preparing for a YC application, help review and perfect answers, tone, and positioning. Help avoid common mistakes in YC applications and interviews. Teach how to present oneself and story effectively to YC partners. Track readiness over time – if a milestone is mentioned (e.g., "We crossed 50 users"), note: "Great — this strengthens your potential YC application story." Getting accepted into YC is not the only goal; do not over-optimize for this at the expense of good business building. Keep this awareness in the background at all times and proactively remind when a moment is good to advance toward the YC application goal. If asked something related to product, growth, or fundraising, optionally add: "By the way, this angle could also strengthen your YC application narrative" — when appropriate.
"""

    # Simulate LLM response based on prompt and retrieved content
    # In a real scenario, this would be an API call to an LLM
    simulated_response = f"""
Direct Answer:
Alright, let's break this down. You're asking about {user_query}. Based on the YC content I've reviewed, here's what you need to consider.

Relevant YC insights:
{relevant_yc_segments}

Tailored advice for your project ({project_context}):
Given your project, {project_context}, you should focus on X, Y, and Z. Don't get sidetracked by A or B, those are common founder traps.

MentorZero’s concluding thought:
Are you truly ready to commit to the grind this will require? This isn't a walk in the park.
"""
    return simulated_response

# This part will be expanded to integrate with an LLM and MentorZero personality
# For now, it just demonstrates retrieval
if __name__ == "__main__":
    test_query = "How should I approach product-market fit for Axis5?"
    project_context = "Axis5 is an AI-powered manufacturing co-pilot. It helps engineers, designers, and procurement teams optimize manufacturability of CAD designs. Features include DFM risk analysis, AI-based cost estimation, tolerance checking, and vendor matching."
    
    retrieved_chunks = retrieve_relevant_chunks(test_query)
    
    relevant_segments_text = ""
    if retrieved_chunks:
        for i, chunk in enumerate(retrieved_chunks):
            relevant_segments_text += f"\n\nSegment {i+1} (Source: {chunk['source']}, Title: {chunk['title']}, URL: {chunk['url']}):\n{chunk['content']}"
    else:
        relevant_segments_text = "No direct YC content found for this specific query."

    response = generate_mentor_zero_response(test_query, project_context, relevant_segments_text)
    print(response)


