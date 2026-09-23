import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
vector_store_id = os.getenv('VECTOR_STORE_ID')

def sync_articles_to_vector_store(processed_articles: list):
  file_paths = [article['file_path'] for article in processed_articles if os.path.exists(article['file_path'])]

  if not file_paths:
    print('No local files to upload')
    return

  file_streams = [open(path, 'rb') for path in file_paths]
  print(f'Uploading {len(file_streams)} files to vector store...')

  file_batch = client.vector_stores.file_batches.upload_and_poll(vector_store_id, files=file_streams)

  for fs in file_streams:
    fs.close()

  print(f'Batch status: {file_batch.status}')
  print(f'File counts: {file_batch.file_counts}')

  return