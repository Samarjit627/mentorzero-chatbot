import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_cbinsights_post_mortems(url, output_dir="./startup_failures"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching startup post-mortems from: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    post_mortems_data = []
    
    # CB Insights page structure might be complex, so we'll look for common article/section tags
    # This is a general approach and might need refinement after inspecting the page HTML
    articles = soup.find_all("div", class_="post-content") or soup.find_all("article")
    
    if not articles:
        # Fallback to body content if specific article divs are not found
        body_content = soup.find("body")
        if body_content:
            article_content = body_content.get_text(separator=" ", strip=True)
            post_mortems_data.append({
                "title": soup.find("title").text if soup.find("title") else "No Title",
                "url": url,
                "content": article_content
            })
    else:
        for article in articles:
            title = article.find("h2") or article.find("h3")
            title_text = title.text.strip() if title else "No Title"
            
            content_tags = article.find_all(["p", "li", "blockquote", "h4", "h5"])
            content = "\n".join([tag.get_text(separator=" ", strip=True) for tag in content_tags])
            
            post_mortems_data.append({
                "title": title_text,
                "url": url, # The URL for individual post-mortems might be different, need to check
                "content": content
            })
            
    with open(os.path.join(output_dir, "startup_failure_post_mortems.json"), "w", encoding="utf-8") as f:
        json.dump(post_mortems_data, f, ensure_ascii=False, indent=4)
    print(f"Scraped {len(post_mortems_data)} post-mortems and saved to ./startup_failures/startup_failure_post_mortems.json")

if __name__ == "__main__":
    scrape_cbinsights_post_mortems("https://www.cbinsights.com/research/startup-failure-post-mortem/")


