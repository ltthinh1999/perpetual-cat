import os
import json

from load_env import MANIFEST_FILE_PATH

def load_manifest():
  if os.path.exists(MANIFEST_FILE_PATH):
    with open(MANIFEST_FILE_PATH, 'r') as f:
      return json.load(f)
  return {}

def save_manifest(manifest):
    with open(MANIFEST_FILE_PATH, 'w') as f:
        json.dump(manifest, f, indent=4)
    return manifest
