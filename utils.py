import os
import json
from config import DUMP_DIR


def ensure_dump_dir():
    os.makedirs(DUMP_DIR, exist_ok=True)


def save_collection(name, documents):
    with open(f"{DUMP_DIR}/{name}.json", "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, default=str)


def load_collection(name):
    with open(f"{DUMP_DIR}/{name}.json", "r", encoding="utf-8") as f:
        return json.load(f)
