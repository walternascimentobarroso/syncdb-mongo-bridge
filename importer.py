from pymongo import MongoClient
from config import LOCAL_URI, LOCAL_DB_NAME, DUMP_DIR
from utils import load_collection
import os
import json


def import_collections(collections=None):
    client = MongoClient(LOCAL_URI)
    db = client[LOCAL_DB_NAME]

    if not collections:
        files = [f for f in os.listdir(DUMP_DIR) if f.endswith(".json")]
        collections = [f.replace(".json", "") for f in files]

    for name in collections:
        try:
            documents = load_collection(name)
            if documents:
                db[name].delete_many({})
                db[name].insert_many(documents, ordered=False)
                print(f"[imported] {name} ({len(documents)} documents)")
            else:
                print(f"[empty] {name}")
        except FileNotFoundError:
            print(f"[not found] {DUMP_DIR}/{name}.json")
        except json.JSONDecodeError:
            print(f"[invalid JSON] {DUMP_DIR}/{name}.json")
        except Exception as e:
            print(f"[error] {name}: {str(e)}")
