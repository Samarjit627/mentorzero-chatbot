import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_yc_blog():
    base_url = "https://www.ycombinator.com"
    blog_url = base_url + "/blog"
    
    print(f"Fetching YC Blog posts from: {blog_url}")
    response = requests.get(blog_url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    blog_posts_data = []
    output_dir = "./yc_blog_posts"
    os.makedirs(output_dir, exist_ok=True)

    # Find all links to individual blog posts
    # This might need adjustment based on the actual HTML structure of the YC blog
    # Looking for <a href="/blog/post-slug">...</a>
    post_links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith('/blog/') and len(href.split('/')) > 2 and not href.endswith('.html'):
            full_url = base_url + href
            post_links.add(full_url)
            
    print(f"Found {len(post_links)} potential blog post links.")
    
    for i, post_url in enumerate(list(post_links)):
        print(f"Scraping blog post {i+1}/{len(post_links)}: {post_url}")
        try:
            post_response = requests.get(post_url)
            post_response.raise_for_status()
            post_soup = BeautifulSoup(post_response.text, 'html.parser')
            
            title = post_soup.find('title').text if post_soup.find('title') else 'No Title'
            
            # Attempt to find the main content area. This is highly dependent on the site's HTML.
            # Common patterns: <article>, <div class="content">, <main>
            content_div = post_soup.find('div', class_='prose') or \
                          post_soup.find('article') or \
                          post_soup.find('main')
            
            article_content = ''
            if content_div:
                # Extract text from common tags within the content area
                content_tags = content_div.find_all(['p', 'h1', 'h2', 'h3', 'li', 'blockquote'])
                article_content = '\n'.join([tag.get_text(separator=' ', strip=True) for tag in content_tags])
            else:
                # Fallback to body content if specific content div not found
                body_content = post_soup.find('body')
                if body_content:
                    article_content = body_content.get_text(separator=' ', strip=True)

            blog_post = {
                "title": title,
                "url": post_url,
                "content": article_content
            }
            blog_posts_data.append(blog_post)
            
            file_name = os.path.join(output_dir, f"{title.replace(' ', '_').replace('/', '_')[:50]}.json")
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(blog_post, f, ensure_ascii=False, indent=4)
            print(f"Saved: {file_name}")

        except Exception as e:
            print(f"Error scraping {post_url}: {e}")
            
    with open(os.path.join(output_dir, "yc_blog_posts.json"), 'w', encoding='utf-8') as f:
        json.dump(blog_posts_data, f, ensure_ascii=False, indent=4)
    print(f"All YC Blog posts scraped and saved to {output_dir}/yc_blog_posts.json")

if __name__ == "__main__":
    scrape_yc_blog()


