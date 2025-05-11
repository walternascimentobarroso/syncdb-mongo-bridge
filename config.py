from dotenv import load_dotenv
import os

load_dotenv()

DUMP_DIR = os.getenv("DUMP_DIR", "dump")

REMOTE_URI = os.getenv("REMOTE_URI")
REMOTE_DB_NAME = os.getenv("REMOTE_DB_NAME")

LOCAL_URI = os.getenv("LOCAL_URI")
LOCAL_DB_NAME = os.getenv("LOCAL_DB_NAME")
