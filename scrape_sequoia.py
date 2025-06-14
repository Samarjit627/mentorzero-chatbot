import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_sequoia_article(url, output_dir="./ai_startup_playbook"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching Sequoia article from: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('title').text if soup.find('title') else 'No Title'
    
    # Sequoia articles typically have the main content within a specific div or article tag
    content_div = soup.find('div', class_='c-richtext') or soup.find('article')
    
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
    file_name = os.path.join(output_dir, f"Sequoia_{safe_title}.json")
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)
    print(f"Saved: {file_name}")
    return article_data

if __name__ == "__main__":
    sequoia_urls = [
        "https://www.sequoiacap.com/article/ai-in-2025/",
        "https://www.sequoiacap.com/article/generative-ai-act-two/",
        "https://one.sequoia.com/2024/04/ai-startups-secure-talent/",
        "https://www.sequoiacap.com/article/pmf-framework/"
    ]
    
    all_sequoia_data = []
    for url in sequoia_urls:
        try:
            data = scrape_sequoia_article(url)
            all_sequoia_data.append(data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            all_sequoia_data.append({
                "title": "Error",
                "url": url,
                "content": f"Failed to scrape: {e}"
            })
            
    with open(os.path.join("./ai_startup_playbook", "sequoia_articles.json"), 'w', encoding='utf-8') as f:
        json.dump(all_sequoia_data, f, ensure_ascii=False, indent=4)
    print(f"All Sequoia articles scraped and saved to ./ai_startup_playbook/sequoia_articles.json")


