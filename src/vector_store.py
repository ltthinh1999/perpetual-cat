import time

from openai import OpenAI

from load_env import OPENAI_API_KEY, VECTOR_STORE_ID

client = OpenAI(api_key=OPENAI_API_KEY)

def sync_articles_to_vector_store(to_add: list, to_update: list, manifest: dict):
  new_manifest = {**manifest}

  for file_to_update in to_update:
    try:
      file_id = new_manifest[file_to_update['id']]['file_id']
      client.vector_stores.files.delete(file_id=file_id, vector_store_id=VECTOR_STORE_ID)
      client.files.delete(file_id)
      time.sleep(0.2)
    except Exception as error:
      print(f'Error deleting file {error}, skipping')
      continue

  articles = to_add + to_update

  if not articles:
    return new_manifest

  uploaded_files = []

  for article in articles:
    try:
      file_stream = open(article['file_path'], 'rb')
      uploaded_file = client.files.create(file=file_stream, purpose='assistants')
      file_stream.close()
      new_manifest[article['id']] = {
        'file_id': uploaded_file.id,
        'updated_at': article['updated_at']
      }
      uploaded_files.append({
        'file_id': uploaded_file.id,
        'attributes': {
          'article_id': article['id']
        }
      })
      time.sleep(0.2)
    except Exception as error:
      continue

  client.vector_stores.file_batches.create_and_poll(vector_store_id=VECTOR_STORE_ID,files=uploaded_files)
  print(f'{len(uploaded_files)} files uploaded')

  return new_manifest