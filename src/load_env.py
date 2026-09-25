import os
import sys

from dotenv import load_dotenv

load_dotenv()

ZENDESK_BASE_URL = os.getenv('ZENDESK_BASE_URL')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
VECTOR_STORE_ID = os.getenv('VECTOR_STORE_ID')
SHOULD_FETCH_ALL_ARTICLES = os.getenv('SHOULD_FETCH_ALL_ARTICLES') == 'True'

def load_env():
  if not ZENDESK_BASE_URL or not OPENAI_API_KEY or not VECTOR_STORE_ID:
    print('Either ZENDESK_BASE_URL, OPENAI_API_KEY or VECTOR_STORE_ID is missing, sync aborted')
    sys.exit(1)

DATA_PATH = 'data'
MANIFEST_FILE_PATH = f'{DATA_PATH}/manifest.json'