import os
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient

load_dotenv()

class BaseService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.mongo = MongoClient(os.getenv("DATABASE_URL"))
        self.db = self.mongo[os.getenv("DATABASE_NAME")]

        self.ensure_indexes()

    def ensure_indexes(self):
        for collection_name in self.db.list_collection_names():
            self.db[collection_name].create_index("tags")