import json
import os
from config import DUMP_DIR


def set_nested_value(obj, key_path, value):
    """
    Sets a value in a nested dictionary given a dot-separated key path.
    Example: set_nested_value(doc, "a.b.c", 123)
    """
    keys = key_path.split(".")
    for key in keys[:-1]:
        obj = obj.setdefault(key, {})
    obj[keys[-1]] = value


def get_nested_value(obj, key_path):
    """
    Retrieves a value from a nested dictionary using a dot-separated key path.
    Returns None if any part of the path is missing.
    """
    keys = key_path.split(".")
    for key in keys:
        if not isinstance(obj, dict) or key not in obj:
            return None
        obj = obj[key]
    return obj


def patch_documents(filter_dict: dict, replacement_dict: dict):
    """
    Applies a filter to all JSON dump files and updates matched documents with new values.
    Supports nested fields using dot-notation.
    """
    for filename in os.listdir(DUMP_DIR):
        if filename.endswith(".json"):
            path = os.path.join(DUMP_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            changed = False
            for doc in data:
                matches = all(get_nested_value(doc, k) == v for k, v in filter_dict.items())
                if matches:
                    for k, v in replacement_dict.items():
                        set_nested_value(doc, k, v)
                    changed = True

            if changed:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, default=str)
                print(f"[patched] {filename}")
