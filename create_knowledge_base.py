import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize the Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_and_chunk_data(file_path, source_type):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    chunks = []
    metadata = []
    
    if isinstance(data, list):
        for item in data:
            content = item.get("content", "")
            url = item.get("url", "N/A")
            title = item.get("title", "N/A")
            
            # Simple chunking by paragraph or sentence
            # For more advanced chunking, consider NLTK or SpaCy
            text_chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
            
            for i, chunk in enumerate(text_chunks):
                chunks.append(chunk)
                metadata.append({"source": source_type, "url": url, "title": title, "chunk_id": i})
    elif isinstance(data, dict):
        content = data.get("content", "")
        url = data.get("url", "N/A")
        title = data.get("title", "N/A")
        
        text_chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
        
        for i, chunk in enumerate(text_chunks):
            chunks.append(chunk)
            metadata.append({"source": source_type, "url": url, "title": title, "chunk_id": i})
            
    return chunks, metadata

def create_faiss_index(chunks, metadata, index_path="faiss_index.bin", metadata_path="faiss_metadata.json"):
    print("Generating embeddings...")
    embeddings = model.encode(chunks, show_progress_bar=True)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
    index.add(embeddings)
    
    faiss.write_index(index, index_path)
    
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)
        
    print(f"FAISS index created and saved to {index_path}")
    print(f"Metadata saved to {metadata_path}")

if __name__ == "__main__":
    all_chunks = []
    all_metadata = []
    
    # Load Paul Graham Essays
    pg_essays_path = "./paul_graham_essays/paul_graham_essays.json"
    if os.path.exists(pg_essays_path):
        chunks, metadata = load_and_chunk_data(pg_essays_path, "Paul Graham Essay")
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)
        print(f"Loaded {len(chunks)} chunks from Paul Graham Essays.")

    # Load YC Blog
    yc_blog_path = "./yc_blog/yc_blog_articles.json"
    if os.path.exists(yc_blog_path):
        chunks, metadata = load_and_chunk_data(yc_blog_path, "YC Blog")
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)
        print(f"Loaded {len(chunks)} chunks from YC Blog.")

    # Load Elad Gil articles
    elad_gil_path = "./investor_thinking/elad_gil_articles.json"
    if os.path.exists(elad_gil_path):
        chunks, metadata = load_and_chunk_data(elad_gil_path, "Elad Gil Article")
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)
        print(f"Loaded {len(chunks)} chunks from Elad Gil Articles.")

    # Load Ben Horowitz articles
    ben_horowitz_path = "./investor_thinking/ben_horowitz_articles.json"
    if os.path.exists(ben_horowitz_path):
        chunks, metadata = load_and_chunk_data(ben_horowitz_path, "Ben Horowitz Article")
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)
        print(f"Loaded {len(chunks)} chunks from Ben Horowitz Articles.")

    # Load Sequoia AI content
    sequoia_ai_path = "./ai_startup_playbook/sequoia_articles.json"
    if os.path.exists(sequoia_ai_path):
        chunks, metadata = load_and_chunk_data(sequoia_ai_path, "Sequoia AI Content")
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)
        print(f"Loaded {len(chunks)} chunks from Sequoia AI Content.")

    # Load YC AI content
    yc_ai_path = "./ai_startup_playbook/yc_ai_articles.json"
    if os.path.exists(yc_ai_path):
        chunks, metadata = load_and_chunk_data(yc_ai_path, "YC AI Content")
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)
        print(f"Loaded {len(chunks)} chunks from YC AI Content.")

    # Load Tren Griffin articles (if available)
    tren_griffin_path = "./investor_thinking/tren_griffin_articles.json"
    if os.path.exists(tren_griffin_path):
        chunks, metadata = load_and_chunk_data(tren_griffin_path, "Tren Griffin Article")
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)
        print(f"Loaded {len(chunks)} chunks from Tren Griffin Articles.")

    # Load Book Summaries (if available)
    book_summaries_path = "./book_summaries/book_summaries.json"
    if os.path.exists(book_summaries_path):
        chunks, metadata = load_and_chunk_data(book_summaries_path, "Book Summary")
        all_chunks.extend(chunks)
        all_metadata.extend(metadata)
        print(f"Loaded {len(chunks)} chunks from Book Summaries.")

    # Create FAISS index
    if all_chunks:
        create_faiss_index(all_chunks, all_metadata)
    else:
        print("No data to create FAISS index.")


