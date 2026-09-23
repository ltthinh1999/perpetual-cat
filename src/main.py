from scraper import fetch_articles, process_articles
from vector_store import sync_articles_to_vector_store

if __name__ == "__main__":
  articles = fetch_articles()
  processed_articles = process_articles(articles)
  sync_articles_to_vector_store(processed_articles)