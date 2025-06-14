import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_elad_gil_blog(url, output_dir="./investor_thinking"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching Elad Gil blog from: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles_data = []
    
    # Find all article links on the main blog page
    # Substack typically has article links within <a> tags with specific classes
    for link in soup.find_all('a', class_='post-preview-image-link'): # This class might need adjustment
        article_url = link.get('href')
        if article_url:
            try:
                print(f"Scraping article: {article_url}")
                article_response = requests.get(article_url)
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                
                title = article_soup.find('h1', class_='post-title').text.strip() if article_soup.find('h1', class_='post-title') else 'No Title'
                
                # Main content is often in a div with class 'primary-post-content' or similar
                content_div = article_soup.find('div', class_='primary-post-content') or article_soup.find('div', class_='body-text')
                
                article_content = ''
                if content_div:
                    content_tags = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'blockquote'])
                    article_content = '\n'.join([tag.get_text(separator=' ', strip=True) for tag in content_tags])
                else:
                    body_content = article_soup.find('body')
                    if body_content:
                        article_content = body_content.get_text(separator=' ', strip=True)

                article_data.append({
                    "title": title,
                    "url": article_url,
                    "content": article_content
                })
                
                safe_title = title.replace(' ', '_').replace('/', '_').replace(':', '_').replace('|', '_').replace('"', '_')[:100]
                file_name = os.path.join(output_dir, f"Elad_Gil_{safe_title}.json")
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(article_data[-1], f, ensure_ascii=False, indent=4)
                print(f"Saved: {file_name}")

            except Exception as e:
                print(f"Error scraping {article_url}: {e}")
                articles_data.append({
                    "title": "Error",
                    "url": article_url,
                    "content": f"Failed to scrape: {e}"
                })
            
    with open(os.path.join(output_dir, "elad_gil_articles.json"), 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=4)
    print(f"All Elad Gil articles scraped and saved to ./investor_thinking/elad_gil_articles.json")

if __name__ == "__main__":
    scrape_elad_gil_blog("https://blog.eladgil.com/")


