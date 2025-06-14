import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_podcast_notes(url, output_dir="./yc_partner_interviews"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching podcast notes from: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('title').text if soup.find('title') else 'No Title'
    
    # Podcast Notes typically has the main content within an <article> tag or a specific div
    content_article = soup.find('article') or soup.find('div', class_='entry-content')
    
    article_content = ''
    if content_article:
        # Extract text from common tags within the content area
        content_tags = content_article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'blockquote'])
        article_content = '\n'.join([tag.get_text(separator=' ', strip=True) for tag in content_tags])
    else:
        # Fallback to body content if specific content div not found
        body_content = soup.find('body')
        if body_content:
            article_content = body_content.get_text(separator=' ', strip=True)

    interview_data = {
        "title": title,
        "url": url,
        "content": article_content
    }
    
    # Sanitize title for filename
    safe_title = title.replace(' ', '_').replace('/', '_').replace(':', '_').replace('|', '_')[:100] # Limit length
    file_name = os.path.join(output_dir, f"{safe_title}.json")
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(interview_data, f, ensure_ascii=False, indent=4)
    print(f"Saved: {file_name}")
    return interview_data

if __name__ == "__main__":
    partner_interview_urls = [
        "https://podcastnotes.org/knowledge-project/garry-tan-billion-dollar-misfits-inside-y-combinators-startup-formula-the-knowledge-project-with-Shane-parrish-226/",
        "https://www.lennysnewsletter.com/p/summary-lessons-from-working-with", # Summary of Gustaf Alströmer interview
        "http://mcj.vc/inevitable-podcast/gustaf-alstromer", # Gustaf Alströmer interview
        "https://joincolossus.com/episode/seibel-lessons-from-thousands-of-startups/", # Michael Seibel interview
        "https://www.theverge.com/22522731/decoder-podcast-michael-seibel-interview-y-combinator-startups" # Michael Seibel interview
    ]
    
    all_interviews_data = []
    for interview_url in partner_interview_urls:
        try:
            data = scrape_podcast_notes(interview_url)
            all_interviews_data.append(data)
        except Exception as e:
            print(f"Error scraping {interview_url}: {e}")
            all_interviews_data.append({
                "title": "Error",
                "url": interview_url,
                "content": f"Failed to scrape: {e}"
            })
            
    with open(os.path.join("./yc_partner_interviews", "yc_partner_interviews_summary.json"), 'w', encoding='utf-8') as f:
        json.dump(all_interviews_data, f, ensure_ascii=False, indent=4)
    print(f"All YC Partner interview notes scraped and saved to ./yc_partner_interviews/yc_partner_interviews_summary.json")


