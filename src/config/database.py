from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConfig:
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql+psycopg2://Aniket:Aniket%402005@localhost:5432/Aniket'
    )

engine = create_engine(DatabaseConfig.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
