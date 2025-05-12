import os
from config import DUMP_DIR
from bson import json_util


def ensure_dump_dir():
    os.makedirs(DUMP_DIR, exist_ok=True)


def save_collection(name, documents):
    with open(f"{DUMP_DIR}/{name}.json", "w", encoding="utf-8") as f:
        f.write(json_util.dumps(documents, indent=2))


def load_collection(name):
    with open(f"{DUMP_DIR}/{name}.json", "r", encoding="utf-8") as f:
        return json_util.loads(f.read())
