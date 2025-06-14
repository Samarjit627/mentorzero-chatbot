import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_startup_school_transcripts():
    base_url = "https://www.ycombinator.com"
    # URL after applying the Startup School filter
    library_search_url = base_url + "/library/search?sus_curriculum=true"
    
    print(f"Fetching Startup School content from: {library_search_url}")
    response = requests.get(library_search_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    transcripts_data = []
    output_dir = "./startup_school_transcripts"
    os.makedirs(output_dir, exist_ok=True)

    # Find all links to individual lessons/transcripts on the search results page
    # Based on manual inspection of the HTML structure of YC Library search results
    # The content links are typically within <a> tags that are children of a div representing a search result item.
    # A common pattern for these content links is that their href starts with /library/ and is not just /library/search
    
    lesson_links = set()
    # Find all div elements that contain the search results. These often have a class like 'ycdc-card' or similar.
    # From the browser view, the results are within a larger container, and each result is a card.
    # Let's look for <a> tags that are direct children of a common parent that holds the result cards.
    
    # A more reliable way is to look for the specific structure of the result cards.
    # Assuming each result card has a link to the content.
    # Let's try to find all <a> tags that have an href starting with '/library/' and are within the main content area.
    
    # The extracted page content in markdown shows links like:
    # [YC's essential startup advice]()
    # [How to succeed with a startup]()
    # These are likely within <a> tags that have the actual content URL.
    
    # Let's try to find all <a> tags that have an href that looks like a content page.
    # The links are typically like /library/some-slug-here
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/library/') and not href.startswith('/library/search') and len(href.split('/')) > 2:
            full_url = base_url + href
            lesson_links.add(full_url)
            
    print(f"Found {len(lesson_links)} potential Startup School lesson links.")
    
    for i, lesson_url in enumerate(list(lesson_links)):
        print(f"Scraping lesson {i+1}/{len(lesson_links)}: {lesson_url}")
        try:
            lesson_response = requests.get(lesson_url)
            lesson_response.raise_for_status()
            lesson_soup = BeautifulSoup(lesson_response.text, 'html.parser')
            
            title = lesson_soup.find('title').text if lesson_soup.find('title') else 'No Title'
            
            # Attempt to find the main content area for the transcript/lesson text
            # Common patterns: <div class="prose">, <article>, <main>
            content_div = lesson_soup.find('div', class_='prose') or \
                          lesson_soup.find('article') or \
                          lesson_soup.find('main')
            
            lesson_content = ''
            if content_div:
                # Extract text from common tags within the content area
                content_tags = content_div.find_all(['p', 'h1', 'h2', 'h3', 'li', 'blockquote'])
                lesson_content = '\n'.join([tag.get_text(separator=' ', strip=True) for tag in content_tags])
            else:
                # Fallback to body content if specific content div not found
                body_content = lesson_soup.find('body')
                if body_content:
                    lesson_content = body_content.get_text(separator=' ', strip=True)

            lesson_data = {
                "title": title,
                "url": lesson_url,
                "content": lesson_content
            }
            transcripts_data.append(lesson_data)
            
            file_name = os.path.join(output_dir, f"{title.replace(' ', '_').replace('/', '_')[:50]}.json")
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(lesson_data, f, ensure_ascii=False, indent=4)
            print(f"Saved: {file_name}")

        except Exception as e:
            print(f"Error scraping {lesson_url}: {e}")
            
    with open(os.path.join(output_dir, "startup_school_transcripts.json"), 'w', encoding='utf-8') as f:
        json.dump(transcripts_data, f, ensure_ascii=False, indent=4)
    print(f"All Startup School transcripts scraped and saved to {output_dir}/startup_school_transcripts.json")

if __name__ == "__main__":
    scrape_startup_school_transcripts()


