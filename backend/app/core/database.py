import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URL or not DB_NAME:
    raise RuntimeError("Missing MongoDB environment variables")

client = MongoClient(
    MONGO_URL,
    serverSelectionTimeoutMS=8000
)

db = client[DB_NAME]
templates_collection = db["templates"]
