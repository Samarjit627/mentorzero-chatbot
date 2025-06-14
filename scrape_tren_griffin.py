import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_tren_griffin_blog(base_url, output_dir="./investor_thinking"):
    os.makedirs(output_dir, exist_ok=True)
    
    all_articles_data = []
    page_num = 1
    while True:
        url = f"{base_url}page/{page_num}/"
        print(f"Fetching Tren Griffin blog from: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Stopped at page {page_num} due to status code {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles_on_page = soup.find_all('article')
        if not articles_on_page:
            print(f"No more articles found on page {page_num}")
            break
            
        for article in articles_on_page:
            title = 'No Title'
            article_url = 'No URL'
            article_content = ''
            try:
                # Try to find title and URL from common structures
                title_tag = article.find('h2', class_='posttitle') or article.find('h2', class_='entry-title')
                if title_tag:
                    link_tag = title_tag.find('a')
                    if link_tag:
                        title = link_tag.text.strip()
                        article_url = link_tag.get('href')
                
                if not article_url or not title:
                    # Fallback: search for any <a> tag within the article that might be the main link
                    fallback_link = article.find('a', href=True)
                    if fallback_link and fallback_link.get('href').startswith('https://25iq.com/'):
                        article_url = fallback_link.get('href')
                        title = fallback_link.text.strip() or 'No Title (Fallback)'

                if not article_url or article_url == 'No URL':
                    print(f"Skipping article due to missing URL: {article.prettify()[:200]}...")
                    continue # Skip this article if URL is still not found

                print(f"Scraping article: {article_url}")
                article_response = requests.get(article_url)
                article_response.raise_for_status()
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                
                content_div = article_soup.find('div', class_='entry-content')
                
                if content_div:
                    content_tags = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'blockquote'])
                    article_content = '\n'.join([tag.get_text(separator=' ', strip=True) for tag in content_tags])
                else:
                    body_content = article_soup.find('body')
                    if body_content:
                        article_content = body_content.get_text(separator=' ', strip=True)

                article_data = {
                    "title": title,
                    "url": article_url,
                    "content": article_content
                }
                all_articles_data.append(article_data)
                
                safe_title = title.replace(' ', '_').replace('/', '_').replace(':', '_').replace('|', '_').replace('"', '_')[:100]
                file_name = os.path.join(output_dir, f"Tren_Griffin_{safe_title}.json")
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(article_data, f, ensure_ascii=False, indent=4)
                print(f"Saved: {file_name}")

            except Exception as e:
                print(f"Error scraping {article_url}: {e}") 
                all_articles_data.append({
                    "title": title,
                    "url": article_url,
                    "content": f"Failed to scrape: {e}"
                })
        page_num += 1
            
    with open(os.path.join(output_dir, "tren_griffin_articles.json"), 'w', encoding='utf-8') as f:
        json.dump(all_articles_data, f, ensure_ascii=False, indent=4)
    print(f"All Tren Griffin articles scraped and saved to ./investor_thinking/tren_griffin_articles.json")

if __name__ == "__main__":
    scrape_tren_griffin_blog("https://25iq.com/author/trengriffin/")


