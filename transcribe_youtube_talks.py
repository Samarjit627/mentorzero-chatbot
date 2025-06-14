import yt_dlp
import whisper
import os
import json

def download_and_transcribe_youtube(video_urls, output_dir="./youtube_transcripts"):
    os.makedirs(output_dir, exist_ok=True)
    model = whisper.load_model("base") # You can choose a larger model like "small", "medium", "large" for better accuracy

    transcripts_data = []

    for i, url in enumerate(video_urls):
        print(f"Processing video {i+1}/{len(video_urls)}: {url}")
        try:
            # Use yt-dlp to get video info and download audio
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
                'quiet': True, # Suppress yt-dlp output
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_id = info_dict.get('id', None)
                video_title = info_dict.get('title', 'No Title')
                upload_date = info_dict.get('upload_date', None) # YYYYMMDD format
                duration = info_dict.get('duration', 0) # in seconds
                
                audio_file = os.path.join(output_dir, f"{video_id}.mp3")
                
                print(f"Transcribing audio for {video_title}...")
                result = model.transcribe(audio_file)
                transcript = result["text"]
                
                transcript_entry = {
                    "video_id": video_id,
                    "title": video_title,
                    "url": url,
                    "published_date": upload_date, # Convert to YYYY-MM-DD later if needed
                    "duration_seconds": duration,
                    "transcript": transcript,
                    "transcript_extracted_yn": "Yes",
                    "ingestion_status": "Success",
                    "last_ingestion_date": os.path.getmtime(audio_file), # Timestamp of file creation
                    "notes": ""
                }
                transcripts_data.append(transcript_entry)
                
                # Save individual transcript
                transcript_file_name = os.path.join(output_dir, f"{video_id}.json")
                with open(transcript_file_name, 'w', encoding='utf-8') as f:
                    json.dump(transcript_entry, f, ensure_ascii=False, indent=4)
                print(f"Saved transcript for {video_title} to {transcript_file_name}")

        except Exception as e:
            print(f"Error processing {url}: {e}")
            transcripts_data.append({
                "video_id": url.split("v=")[-1] if "v=" in url else url, # Attempt to get ID even on failure
                "title": "Error",
                "url": url,
                "published_date": "N/A",
                "duration_seconds": 0,
                "transcript": "",
                "transcript_extracted_yn": "No",
                "ingestion_status": "Failed",
                "last_ingestion_date": "N/A",
                "notes": str(e)
            })
            
    with open(os.path.join(output_dir, "youtube_transcripts_summary.json"), 'w', encoding='utf-8') as f:
        json.dump(transcripts_data, f, ensure_ascii=False, indent=4)
    print(f"All YouTube transcripts summary saved to {output_dir}/youtube_transcripts_summary.json")

if __name__ == "__main__":
    # List of Paul Graham YouTube talks/interviews found from web search
    paul_graham_youtube_urls = [
        "https://www.youtube.com/watch?v=YMqgiXLjvRs", # Y Combinator's Paul Graham sits down with Jason at ...
        "https://www.youtube.com/watch?v=3mAd5LJFdb4", # Paul Graham on Start-ups, Innovation, and Creativity
        "https://www.youtube.com/watch?v=ii1jcLg-eIQ", # Lecture 3 - Before the Startup (Paul Graham)
        "https://www.youtube.com/watch?v=AJb4u8MoqxY", # Startups - Great Way to Raise Money but They Hurt! | Paul ...
        "https://www.youtube.com/watch?v=4WO5kJChg3w"  # A Conversation with Paul Graham - Moderated by Geoff Ralston
    ]
    
    download_and_transcribe_youtube(paul_graham_youtube_urls, output_dir="./paul_graham_talks")


