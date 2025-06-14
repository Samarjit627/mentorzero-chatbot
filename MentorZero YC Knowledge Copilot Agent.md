# MentorZero YC Knowledge Copilot Agent

This document provides instructions on how to use and interact with the MentorZero YC Knowledge Copilot Agent. MentorZero is designed to act as a seasoned founder and mentor, providing direct, honest, and constructively critical advice grounded in Y Combinator's teachings and other relevant startup wisdom.

## Project Structure

- `scrape_paul_graham.py`: Script to scrape Paul Graham essays.
- `scrape_yc_blog.py`: Script to scrape YC Blog articles.
- `scrape_yc_partner_interviews.py`: Script to scrape YC Partner interview notes.
- `scrape_book_summaries.py`: Script to scrape summaries of YC Recommended Books.
- `scrape_a16z.py`: Script to scrape articles from a16z.
- `scrape_elad_gil.py`: Script to scrape articles from Elad Gil's blog.
- `scrape_tren_griffin.py`: Script to scrape articles from Tren Griffin's blog.
- `scrape_yc_ai.py`: Script to scrape YC AI startup content.
- `create_knowledge_base.py`: Script to chunk data from all scraped sources and create a FAISS vector index.
- `rag_logic.py`: Contains the core Retrieval-Augmented Generation (RAG) logic, including the MentorZero personality integration and a placeholder for LLM interaction.
- `weekly_update.py`: Automates the scraping, knowledge base creation, and ingestion report generation.
- `faiss_index.bin`: The FAISS vector index containing embeddings of the knowledge base.
- `faiss_metadata.json`: Metadata corresponding to the FAISS index, linking embeddings back to their original content and source.
- `yc_video_ingestion_report.csv`: A transparency report detailing the ingested content (currently a placeholder for YouTube content).

## How to Use MentorZero

### 1. Initial Setup (Already Completed)

All necessary Python packages (`yt-dlp`, `openai-whisper`, `requests`, `beautifulsoup4`, `faiss-cpu`, `sentence-transformers`) have been installed.

### 2. Knowledge Base

The knowledge base has been created using the `create_knowledge_base.py` script, which processes content from:

- Paul Graham Essays
- YC Blog
- Elad Gil's blog
- Ben Horowitz's blog
- Selected Sequoia Capital AI content
- Selected YC AI content
- Tren Griffin's blog
- YC Recommended Book summaries

**Note on Content Limitations:**

Due to anti-bot measures and complex website structures, direct scraping of the following sources proved challenging and was not fully successful:

- YC YouTube Channel (full video list and transcripts via `yt-dlp` and `openai-whisper`)
- YC Podcast transcripts
- YC Startup School transcripts
- CB Insights (for startup failure post-mortems)

Alternative methods or manual data collection would be required for these sources if comprehensive coverage is critical. The current knowledge base is built from the successfully scraped web content.

### 3. Running the Chat Interface (Example)

To interact with MentorZero, you would typically integrate the `rag_logic.py` with an LLM API and a user interface. Below is a simplified example of how you might run a local chat interface using the existing `rag_logic.py`.

First, ensure you have an LLM API key configured (e.g., OpenAI, Google Gemini, Claude). For this example, we'll use a placeholder for the LLM response, as direct LLM integration is beyond the scope of this deliverable.

```python
# chat_interface.py

import os
import sys
import json

# Add the current directory to the Python path to import rag_logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_logic import retrieve_relevant_chunks, generate_mentor_zero_response

def main():
    print("\n--- Welcome to MentorZero ---")
    print("Type 'exit' to quit.")
    
    # Placeholder for user's project context. In a real application, this would be dynamic.
    project_context = "Axis5 is an AI-powered manufacturing co-pilot. It helps engineers, designers, and procurement teams optimize manufacturability of CAD designs. Features include DFM risk analysis, AI-based cost estimation, tolerance checking, and vendor matching. My long-term goal is YC acceptance."

    while True:
        user_query = input("\nYour question: ")
        if user_query.lower() == 'exit':
            break

        # Retrieve relevant chunks from the knowledge base
        retrieved_chunks = retrieve_relevant_chunks(user_query)
        
        relevant_segments_text = ""
        if retrieved_chunks:
            for i, chunk in enumerate(retrieved_chunks):
                relevant_segments_text += f"\n\nSegment {i+1} (Source: {chunk.get("source", "N/A")}, Title: {chunk.get("title", "N/A")}, URL: {chunk.get("url", "N/A")}):\n{chunk.get("content", "")}"
        else:
            relevant_segments_text = "No direct relevant content found in the knowledge base for this query."

        # Generate MentorZero's response
        # IMPORTANT: This currently uses a simulated LLM response. 
        # In a real application, you would replace this with an actual LLM API call.
        mentor_zero_response = generate_mentor_zero_response(user_query, project_context, relevant_segments_text)
        
        print("\nMentorZero:")
        print(mentor_zero_response)

if __name__ == "__main__":
    main()
```

To run this example chat interface:

1.  Save the code above as `chat_interface.py` in the same directory as your other scripts.
2.  Open a terminal in that directory.
3.  Run the script: `python3 chat_interface.py`

### 4. Auto-Updater and Transparency

-   **`weekly_update.py`**: This script automates the process of re-running all scraping scripts, updating the FAISS knowledge base, and generating the `yc_video_ingestion_report.csv`.
-   **Scheduled Task**: A weekly cron job named "MentorZero Weekly Knowledge Base Update" has been scheduled to run `weekly_update.py`. **Please note that this scheduled task is currently not enabled and requires a user account upgrade to activate.** Without activation, the knowledge base will not automatically update.
-   **`yc_video_ingestion_report.csv`**: This CSV file provides transparency into the ingested content. It includes details like Video ID, URL, Title, Published Date, Duration, Transcript Tokens, Extraction Status, Ingestion Status, Last Ingestion Date, and Notes. Currently, it contains placeholders for YouTube content due to scraping limitations, but it accurately reflects the status of other ingested web content.

    You can view this file to audit the knowledge base. In a fully integrated system, the `/videosummary` and `/checkvideo [URL]` commands would query this data to provide real-time verification within the chat interface.

## Next Steps

To further enhance MentorZero, you would integrate a real LLM (e.g., OpenAI's GPT-4o, Claude 3.5 Sonnet) into `rag_logic.py` and `chat_interface.py`. This would allow for dynamic, intelligent responses based on the retrieved knowledge and the MentorZero personality. You would also need to consider a more robust deployment strategy for the chat interface (e.g., Streamlit, Flask app, or a custom UI).

I have provided all the necessary scripts and a working knowledge base. Please let me know if you have any further questions or require assistance with specific integrations.

