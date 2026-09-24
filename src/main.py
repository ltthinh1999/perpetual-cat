import time
from scraper import fetch_articles
from processor import process_articles
from vector_store import sync_articles_to_vector_store, construct_manifest_from_vector_store
from load_env import load_env

if __name__ == "__main__":
  load_env()

  start_time = time.time()

  articles = fetch_articles(should_fetch_all=False)
  manifest = construct_manifest_from_vector_store()
  [to_add, to_update] = process_articles(articles, manifest)
  sync_articles_to_vector_store(to_add, to_update, manifest)

  print(f'Elapsed time: {time.time() - start_time}s')