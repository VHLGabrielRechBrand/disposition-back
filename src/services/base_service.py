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