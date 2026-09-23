import os
import re
import requests
from markdownify import markdownify as md
from dotenv import load_dotenv

load_dotenv()

ZENDESK_BASE_URL = os.getenv('ZENDESK_BASE_URL')

def slugify(text):
    trimmed = text.lower().strip()
    removed_special_chars = re.sub(r'[^\w\s-]', '', trimmed)
    return re.sub(r'[-\s]+', '-', removed_special_chars)

def fetch_articles():
    ARTICLES_URL = f'{ZENDESK_BASE_URL}/api/v2/help_center/articles'
    print(f'Fetching articles...')
    response = requests.get(ARTICLES_URL, {
        'sort_by': 'position',
        'sort_order': 'asc',
        'page': 1,
        'per_page': 100,
    })
    if response.status_code != 200:
        print('Failed to fetch articles from Zendesk API.')
        return []
    
    return response.json().get('articles', [])

def process_articles(articles: list):
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    processed_articles = []
    for art in articles:
        # Skip empty or draft articles
        if not art.get('body') or art.get('draft'):
            continue
            
        title = art['title']
        slug = slugify(title)
        html_body = art['body']
        url = art['html_url']
        updated_at = art['updated_at']

        # Append source metadata to the top of the body for RAG references
        full_html = f'<h1>{title}</h1><p><strong>Article URL:</strong> {url}</p>{html_body}'
        
        markdown_content = md(full_html, heading_style='ATX')
        
        file_path = os.path.join(output_dir, f'{slug}.md')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        processed_articles.append({
            'id': art['id'],
            'slug': slug,
            'file_path': file_path,
            'updated_at': updated_at,
            'url': url
        })
        
    print(f'Successfully saved {len(processed_articles)} markdown articles.')
    return processed_articles
