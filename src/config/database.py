from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConfig:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    DB_NAME = os.getenv('DB_NAME', 'resume_analyzer')

    @staticmethod
    def get_client():
        return MongoClient(DatabaseConfig.MONGO_URI)

    @staticmethod
    def get_database():
        client = DatabaseConfig.get_client()
        return client[DatabaseConfig.DB_NAME]