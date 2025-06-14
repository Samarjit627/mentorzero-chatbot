import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_paul_graham_essays():
    base_url = "https://paulgraham.com/"
    articles_page_url = base_url + "articles.html"
    
    print(f"Fetching articles from: {articles_page_url}")
    response = requests.get(articles_page_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all links that point to articles (usually .html files in the same directory)
    # This might need adjustment based on the actual HTML structure
    article_links = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.endswith('.html') and not href.startswith('http') and '/' not in href:
            article_links.append(base_url + href)
            
    print(f"Found {len(article_links)} potential article links.")
    
    essays_data = []
    output_dir = "./paul_graham_essays"
    os.makedirs(output_dir, exist_ok=True)

    for i, article_url in enumerate(article_links):
        print(f"Scraping article {i+1}/{len(article_links)}: {article_url}")
        try:
            article_response = requests.get(article_url)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            
            # Extract title - this might vary, common tags are <title>, <h1>
            title = article_soup.find('title').text if article_soup.find('title') else 'No Title'
            
            # Extract content - usually within <p> tags or a specific div/main tag
            # This is a generic approach, might need refinement for specific articles
            content_tags = article_soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])
            article_content = '\n'.join([tag.get_text(separator=' ', strip=True) for tag in content_tags])
            
            if not article_content.strip():
                # Fallback for content if initial tags don't yield much
                body_content = article_soup.find('body')
                if body_content:
                    article_content = body_content.get_text(separator=' ', strip=True)

            essay = {
                "title": title,
                "url": article_url,
                "content": article_content
            }
            essays_data.append(essay)
            
            # Save each essay to a separate file for easier processing later
            file_name = os.path.join(output_dir, f"{title.replace(' ', '_').replace('/', '_')[:50]}.json")
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(essay, f, ensure_ascii=False, indent=4)
            print(f"Saved: {file_name}")

        except Exception as e:
            print(f"Error scraping {article_url}: {e}")
            
    with open(os.path.join(output_dir, "paul_graham_essays.json"), 'w', encoding='utf-8') as f:
        json.dump(essays_data, f, ensure_ascii=False, indent=4)
    print(f"All Paul Graham essays scraped and saved to {output_dir}/paul_graham_essays.json")

if __name__ == "__main__":
    scrape_paul_graham_essays()


