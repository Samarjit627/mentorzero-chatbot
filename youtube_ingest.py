import os
import csv
import json
import requests
from datetime import datetime
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript

YOUTUBE_API_KEY = "AIzaSyBxKXJmekWRJAq-oBch64exY-6qxkXc_a8"  # Use securely for MentorZero ingestion only
YC_CHANNEL_ID = "UCcefcZRL2oaA_uBNeo5UOWg"  # Official YC channel
REPORT_CSV = "yc_video_ingestion_report.csv"
TRANSCRIPTS_DIR = "./yc_youtube_transcripts"

os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)

def get_yc_videos(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = {}

    # 1. Fetch all videos from the main uploads
    next_page_token = None
    while True:
        req = youtube.search().list(
            channelId=channel_id,
            part='id,snippet',
            maxResults=50,
            order='date',
            type='video',
            pageToken=next_page_token
        )
        res = req.execute()
        for item in res['items']:
            video_id = item['id']['videoId']
            videos[video_id] = {
                'video_id': video_id,
                'title': item['snippet']['title'],
                'published_at': item['snippet']['publishedAt'],
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'source': 'Uploads'
            }
        next_page_token = res.get('nextPageToken')
        if not next_page_token:
            break

    # 2. Fetch all public playlists
    playlist_ids = []
    next_page_token = None
    while True:
        pl_req = youtube.playlists().list(
            channelId=channel_id,
            part='id,snippet',
            maxResults=50,
            pageToken=next_page_token
        )
        pl_res = pl_req.execute()
        for pl in pl_res['items']:
            playlist_ids.append(pl['id'])
        next_page_token = pl_res.get('nextPageToken')
        if not next_page_token:
            break

    # 3. Fetch all videos from each playlist
    for playlist_id in playlist_ids:
        next_page_token = None
        while True:
            pv_req = youtube.playlistItems().list(
                playlistId=playlist_id,
                part='contentDetails,snippet',
                maxResults=50,
                pageToken=next_page_token
            )
            pv_res = pv_req.execute()
            for item in pv_res['items']:
                video_id = item['contentDetails']['videoId']
                # Avoid duplicates, but note if found in both uploads and playlists
                if video_id not in videos:
                    videos[video_id] = {
                        'video_id': video_id,
                        'title': item['snippet']['title'],
                        'published_at': item['snippet'].get('publishedAt', ''),
                        'url': f'https://www.youtube.com/watch?v={video_id}',
                        'source': f'Playlist: {playlist_id}'
                    }
                else:
                    # Mark that this video is also in a playlist
                    if 'also_in_playlists' not in videos[video_id]:
                        videos[video_id]['also_in_playlists'] = []
                    videos[video_id]['also_in_playlists'].append(playlist_id)
            next_page_token = pv_res.get('nextPageToken')
            if not next_page_token:
                break

    print(f"Total unique videos found (Uploads + Playlists): {len(videos)}")
    return list(videos.values())

def get_video_metadata(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    req = youtube.videos().list(
        part='snippet,contentDetails',
        id=video_id
    )
    res = req.execute()
    if not res['items']:
        return {}
    item = res['items'][0]
    return {
        'title': item['snippet']['title'],
        'description': item['snippet'].get('description', ''),
        'published_at': item['snippet']['publishedAt'],
        'duration': item['contentDetails']['duration']
    }

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return '\n'.join([seg['text'] for seg in transcript]), 'Yes', ''
    except (TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript) as e:
        return '', 'No', str(e)
    except Exception as e:
        return '', 'No', f'Unknown error: {e}'

def save_transcript_json(video_id, title, url, published_at, transcript):
    data = {
        'video_id': video_id,
        'title': title,
        'url': url,
        'published_at': published_at,
        'transcript': transcript
    }
    fname = os.path.join(TRANSCRIPTS_DIR, f'{video_id}.json')
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    print("Fetching YC YouTube video list...")
    videos = get_yc_videos(YOUTUBE_API_KEY, YC_CHANNEL_ID)
    print(f"Found {len(videos)} videos.")
    report_rows = []
    for i, video in enumerate(videos):
        print(f"[{i+1}/{len(videos)}] Processing {video['title']} ({video['url']})")
        meta = get_video_metadata(YOUTUBE_API_KEY, video['video_id'])
        transcript, transcript_extracted_yn, notes = get_transcript(video['video_id'])
        save_transcript_json(
            video['video_id'],
            video['title'],
            video['url'],
            video['published_at'],
            transcript
        )
        report_rows.append({
            'Source': 'YC YouTube',
            'Video Title': video['title'],
            'URL': video['url'],
            'Published Date': video['published_at'],
            'Transcript Tokens': len(transcript.split()),
            'Transcript Extracted Y/N': transcript_extracted_yn,
            'Ingestion Status': 'Success' if transcript_extracted_yn == 'Yes' else 'Failed',
            'Last Ingestion Date': datetime.now().isoformat(),
            'Notes': notes
        })
    # Write CSV report
    with open(REPORT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Source', 'Video Title', 'URL', 'Published Date', 'Transcript Tokens', 'Transcript Extracted Y/N', 'Ingestion Status', 'Last Ingestion Date', 'Notes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in report_rows:
            writer.writerow(row)
    print(f"Report written to {REPORT_CSV}")

if __name__ == "__main__":
    main()
