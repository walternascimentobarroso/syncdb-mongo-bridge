from pymongo import MongoClient
from config import REMOTE_URI, REMOTE_DB_NAME
from utils import ensure_dump_dir, save_collection


def export_collections(collections=None, query={}):
    client = MongoClient(REMOTE_URI, serverSelectionTimeoutMS=60000, socketTimeoutMS=60000)
    db = client[REMOTE_DB_NAME]

    ensure_dump_dir()
    if not collections:
        collections = db.list_collection_names()

    for name in collections:
        documents = list(db[name].find(query))
        if documents:
            save_collection(name, documents)
            print(f"[exported] {name} ({len(documents)} documents)")
        else:
            print(f"[empty] {name}")
