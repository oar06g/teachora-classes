from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from src.config import engine
from enum import Enum
import asyncio

Base = declarative_base()

class Gender(str, Enum):
  male = "male"
  female = "female"

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, autoincrement=True)
  full_name = Column(String(100), nullable=False)
  username = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)
  gender = Column(String(10), nullable=False)
  email = Column(String(100), nullable=False, unique=True)
  token = Column(String(100), nullable=False)
  is_teacher = Column(Boolean, default=False)
  profile_img = Column(String(255), default="/assets/images/profile_img_male.jpg")


class Student(Base):
  __tablename__ = "students"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  grade = Column(String(70), nullable=False)
  level = Column(String(70), nullable=False)


class Teacher(Base):
  __tablename__ = "teachers"
  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  study_material = Column(String(70), nullable=False)
  certificate = Column(String(255), nullable=False)


async def create_tables():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)


async def main():
  await create_tables()


if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print("Ctrl + C")
