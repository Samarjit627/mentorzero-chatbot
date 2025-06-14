import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_musixmatch_podcast_transcripts(podcast_url, output_dir="./yc_podcast_transcripts"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching podcast episodes from: {podcast_url}")
    response = requests.get(podcast_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    episode_links = []
    # Musixmatch podcast pages typically have links to individual episode pages
    # Look for links that contain '/episode/' in their href
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/episode/' in href and href.startswith('/podcast/'):
            full_url = f"https://podcasts.musixmatch.com{href}"
            episode_links.append(full_url)
            
    print(f"Found {len(episode_links)} potential podcast episode links.")
    
    transcripts_data = []

    for i, episode_url in enumerate(episode_links):
        print(f"Scraping episode {i+1}/{len(episode_links)}: {episode_url}")
        try:
            episode_response = requests.get(episode_url)
            episode_response.raise_for_status()
            episode_soup = BeautifulSoup(episode_response.text, 'html.parser')
            
            title = episode_soup.find('title').text if episode_soup.find('title') else 'No Title'
            
            # Transcripts are often in a specific div or section
            # This might need adjustment based on Musixmatch's HTML structure
            transcript_div = episode_soup.find('div', class_='mxm-transcription-card__content') or \
                             episode_soup.find('div', class_='transcript-content')
            
            transcript_text = ''
            if transcript_div:
                transcript_text = transcript_div.get_text(separator=' ', strip=True)
            else:
                # Fallback if specific div not found
                body_content = episode_soup.find('body')
                if body_content:
                    transcript_text = body_content.get_text(separator=' ', strip=True)

            episode_data = {
                "title": title,
                "url": episode_url,
                "content": transcript_text
            }
            transcripts_data.append(episode_data)
            
            file_name = os.path.join(output_dir, f"{title.replace(' ', '_').replace('/', '_')[:50]}.json")
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(episode_data, f, ensure_ascii=False, indent=4)
            print(f"Saved: {file_name}")

        except Exception as e:
            print(f"Error scraping {episode_url}: {e}")
            
    with open(os.path.join(output_dir, "yc_podcast_transcripts.json"), 'w', encoding='utf-8') as f:
        json.dump(transcripts_data, f, ensure_ascii=False, indent=4)
    print(f"All YC Podcast transcripts scraped and saved to {output_dir}/yc_podcast_transcripts.json")

if __name__ == "__main__":
    # URL for Y Combinator Startup Podcast on Musixmatch
    yc_podcast_musixmatch_url = "https://podcasts.musixmatch.com/podcast/y-combinator-01h77tzyn0cr0kd0acnjbwh2ke"
    scrape_musixmatch_podcast_transcripts(yc_podcast_musixmatch_url)


