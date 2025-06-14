import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_yc_ai_content(url, output_dir="./ai_startup_playbook"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching YC AI content from: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.find("title").text if soup.find("title") else "No Title"
    
    # Attempt to find the main content area, common classes for articles/blogs
    content_div = soup.find("div", class_="post-content") or \
                  soup.find("article") or \
                  soup.find("div", class_="content") or \
                  soup.find("div", class_="markdown-body")
    
    article_content = ""
    if content_div:
        content_tags = content_div.find_all(["p", "h1", "h2", "h3", "h4", "li", "blockquote"])
        article_content = "\n".join([tag.get_text(separator=" ", strip=True) for tag in content_tags])
    else:
        body_content = soup.find("body")
        if body_content:
            article_content = body_content.get_text(separator=" ", strip=True)

    article_data = {
        "title": title,
        "url": url,
        "content": article_content
    }
    
    safe_title = title.replace(" ", "_").replace("/", "_").replace(":", "_").replace("|", "_").replace("\"", "_")[:100]
    file_name = os.path.join(output_dir, f"YC_AI_{safe_title}.json")
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(article_data, f, ensure_ascii=False, indent=4)
    print(f"Saved: {file_name}")
    return article_data

if __name__ == "__main__":
    yc_ai_urls = [
        "https://www.ycombinator.com/companies/industry/ai", # This is a directory, will get general info
        "https://www.ycombinator.com/companies/industry/generative-ai", # Another directory
        "https://www.businessinsider.com/y-combinator-yc-demo-day-spring-ai-agent-startups-2025-6", # Article
        "https://pitchbook.com/news/articles/y-combinator-is-going-all-in-on-ai-agents-making-up-nearly-50-of-latest-batch", # Article
        "https://dswharshit.medium.com/what-you-should-build-with-ai-analyzing-400-ai-startups-backed-by-ycombinator-9782237755f3", # Medium article
        "https://cloud.google.com/blog/topics/startups/supporting-y-combinator-ai-startups-with-google-cloud-technology" # Blog post
    ]
    
    all_yc_ai_data = []
    for url in yc_ai_urls:
        try:
            data = scrape_yc_ai_content(url)
            all_yc_ai_data.append(data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            all_yc_ai_data.append({
                "title": "Error",
                "url": url,
                "content": f"Failed to scrape: {e}"
            })
            
    with open(os.path.join("./ai_startup_playbook", "yc_ai_articles.json"), "w", encoding="utf-8") as f:
        json.dump(all_yc_ai_data, f, ensure_ascii=False, indent=4)
    print(f"All YC AI articles scraped and saved to ./ai_startup_playbook/yc_ai_articles.json")


