import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_a16z_article(url, output_dir="./investor_thinking"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching a16z article from: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('title').text if soup.find('title') else 'No Title'
    
    # A16z articles typically have the main content within a specific div or article tag
    content_div = soup.find('div', class_='single-content') or soup.find('article')
    
    article_content = ''
    if content_div:
        # Extract text from common tags within the content area
        content_tags = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'blockquote'])
        article_content = '\n'.join([tag.get_text(separator=' ', strip=True) for tag in content_tags])
    else:
        # Fallback to body content if specific content div not found
        body_content = soup.find('body')
        if body_content:
            article_content = body_content.get_text(separator=' ', strip=True)

    article_data = {
        "title": title,
        "url": url,
        "content": article_content
    }
    
    # Sanitize title for filename
    safe_title = title.replace(' ', '_').replace('/', '_').replace(':', '_').replace('|', '_').replace('"', '_')[:100] # Limit length
    file_name = os.path.join(output_dir, f"{safe_title}.json")
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)
    print(f"Saved: {file_name}")
    return article_data

if __name__ == "__main__":
    a16z_urls = [
        "https://a16z.com/its-time-to-build/",
        "https://a16z.com/why-software-is-eating-the-world/",
        "https://a16z.com/making-yourself-a-ceo/",
        "https://a16z.com/the-techno-optimist-manifesto/",
        "https://a16z.com/ai-will-save-the-world/"
    ]
    
    all_a16z_data = []
    for url in a16z_urls:
        try:
            data = scrape_a16z_article(url)
            all_a16z_data.append(data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            all_a16z_data.append({
                "title": "Error",
                "url": url,
                "content": f"Failed to scrape: {e}"
            })
            
    with open(os.path.join("./investor_thinking", "a16z_articles.json"), 'w', encoding='utf-8') as f:
        json.dump(all_a16z_data, f, ensure_ascii=False, indent=4)
    print(f"All a16z articles scraped and saved to ./investor_thinking/a16z_articles.json")


