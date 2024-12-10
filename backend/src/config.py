from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import os

load_dotenv()
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
database = os.getenv("DB_NAME")
port = os.getenv("PORT")
encryption_password = os.getenv("ENCRYPTION_PASSWORD")

DATABASE_URL = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
  async with SessionLocal() as db:
    yield db
