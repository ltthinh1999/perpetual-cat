import re
import requests

from load_env import ZENDESK_BASE_URL

ARTICLES_URL = f'{ZENDESK_BASE_URL}/api/v2/help_center/articles'

def slugify(text):
    trimmed = text.lower().strip()
    removed_special_chars = re.sub(r'[^\w\s-]', '', trimmed)
    return re.sub(r'[-\s]+', '-', removed_special_chars)

def fetch_articles_page(page: int):
    return requests.get(ARTICLES_URL, {
        'sort_by': 'updated_at',
        'page': page,
        'per_page': 50,
    })

def fetch_articles(should_fetch_all: bool):
    print(f'Fetching articles...')
    articles = []
    current_page = 1
    should_load_more = True

    try:
        initial_response = fetch_articles_page(page=current_page)
        initial_response.raise_for_status()
        current_response = initial_response.json()
        current_page += 1
        articles.extend(current_response.get('articles', []))
        should_load_more = should_fetch_all and current_response.get('page_count', 1) > current_page
    except requests.exceptions.HTTPError as err:
        return articles

    if not should_fetch_all:
        return articles

    while should_load_more:
        try:
            response = fetch_articles_page(page=current_page)
            response.raise_for_status()
            current_response = response.json()
            should_load_more = current_response.get('page_count', 1) > current_page
            current_page += 1
            articles.extend(current_response.get('articles', []))
        except requests.exceptions.HTTPError as err:
            return articles    

    return articles
