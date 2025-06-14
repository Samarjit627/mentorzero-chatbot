import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_book_summary(url, book_title, output_dir="./book_summaries"):
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Fetching summary for \'{book_title}\' from: {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('title').text if soup.find('title') else 'No Title' # Moved title definition here

    # Attempt to find the main content area for the summary
    # This will require inspection of the actual page HTML for each site
    # For wilselby.com, the main content seems to be within an article tag or a div with specific class
    content_div = soup.find('article') or soup.find('div', class_='entry-content') or soup.find('div', class_='post-content')
    
    summary_content = ''
    if content_div:
        # Extract text from common tags within the content area
        content_tags = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'li', 'blockquote'])
        summary_content = '\n'.join([tag.get_text(separator=' ', strip=True) for tag in content_tags])
    else:
        # Fallback to body content if specific content div not found
        body_content = soup.find('body')
        if body_content:
            summary_content = body_content.get_text(separator=' ', strip=True)

    book_data = {
        "title": book_title,
        "url": url,
        "content": summary_content
    }
    
    # Sanitize title for filename
    safe_title = title.replace(' ', '_').replace('/', '_').replace(':', '_').replace('|', '_')[:100] # Limit length
    file_name = os.path.join(output_dir, f"{safe_title}.json")
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(book_data, f, ensure_ascii=False, indent=4)
    print(f"Saved: {file_name}")
    return book_data

if __name__ == "__main__":
    books_to_scrape = [
        {
            "title": "The Mom Test",
            "url": "https://wilselby.com/2020/06/the-mom-test-summary-and-insights/"
        },
        {
            "title": "High Output Management",
            "url": "https://www.goodreads.com/book/show/324750.High_Output_Management"
        },
        {
            "title": "Founder’s Dilemmas",
            "url": "https://sobrief.com/books/the-founders-dilemmas"
        },
        {
            "title": "7 Powers",
            "url": "https://blas.com/7-powers/"
        },
        {
            "title": "The Lean Startup",
            "url": "https://clickup.com/blog/the-lean-startup-summary/" # Changed URL to a more reliable source
        }
    ]
    
    all_book_summaries = []
    for book in books_to_scrape:
        try:
            data = scrape_book_summary(book["url"], book["title"])
            all_book_summaries.append(data)
        except Exception as e:
            print(f"Error scraping {book['url']}: {e}")
            all_book_summaries.append({
                "title": book["title"],
                "url": book["url"],
                "content": f"Failed to scrape: {e}"
            })
            
    with open(os.path.join("./book_summaries", "yc_recommended_books_summaries.json"), 'w', encoding='utf-8') as f:
        json.dump(all_book_summaries, f, ensure_ascii=False, indent=4)
    print(f"All YC Recommended Book summaries scraped and saved to ./book_summaries/yc_recommended_books_summaries.json")

