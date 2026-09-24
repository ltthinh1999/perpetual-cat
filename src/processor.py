import os
import re

from markdownify import markdownify as md
from datetime import datetime
from load_env import DATA_PATH

def slugify(text):
    trimmed = text.lower().strip()
    removed_special_chars = re.sub(r'[^\w\s-]', '', trimmed)
    return re.sub(r'[-\s]+', '-', removed_special_chars)

def get_date_time(timestamp: str):
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

def process_articles(articles: list, manifest: dict):
    os.makedirs(DATA_PATH, exist_ok=True)
    to_update = []
    to_add = []
    added, updated, skipped = 0, 0, 0
    for article in articles:
        # Skip empty or draft articles
        if not article['body'] or article['draft']:
          skipped += 1
          continue

        id = str(article['id'])
        updated_at = article['updated_at']

        existing_manifest = manifest.get(id)

        if existing_manifest and get_date_time(existing_manifest['updated_at']) == get_date_time(updated_at):
          skipped += 1
          continue

        title = article['title']
        slug = f'{id}-{slugify(title)}'
        html_body = article['body']
        url = article['html_url']

        # Append source metadata to the top of the body for RAG references
        full_html = f'<h1>{title}</h1><p><strong>Article URL:</strong> {url}</p>{html_body}'
        
        markdown_content = md(full_html, heading_style='ATX')
        
        file_path = os.path.join(DATA_PATH, f'{slug}.md')
        with open(file_path, 'w', encoding='utf-8') as f:
          f.write(markdown_content)

        processed_article = {
          'id': id,
          'slug': slug,
          'file_path': file_path,
          'updated_at': updated_at,
          'url': url,
          'markdown_content': markdown_content
        }

        if not existing_manifest:
          added += 1
          to_add.append(processed_article)
        else:
          updated += 1
          to_update.append(processed_article)

    print(f'Added: {added}\nUpdated: {updated}\nSkipped: {skipped}')
    return [to_add, to_update]
