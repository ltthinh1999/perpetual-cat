import time
from scraper import fetch_articles
from processor import process_articles
from manifest import load_manifest, save_manifest
from vector_store import sync_articles_to_vector_store
from load_env import load_env

if __name__ == "__main__":
  load_env()

  start_time = time.time()
  articles = fetch_articles(should_fetch_all=False)
  manifest = load_manifest()
  [to_add, to_update] = process_articles(articles)
  new_manifest = sync_articles_to_vector_store(to_add, to_update, manifest)
  save_manifest(new_manifest)

  print(f'Elapsed time: {time.time() - start_time}s')