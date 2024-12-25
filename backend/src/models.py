from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Date
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
    certificate = Column(String(255), nullable=True)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(100), nullable=False)  # اسم الدورة
    description = Column(String(700), nullable=False)  # وصف الدورة
    lesson_price = Column(Float, nullable=False)  # سعر الحصة بالجنيه المصري
    material = Column(String(100), nullable=False)  # المواد الدراسية
    level = Column(String(50), nullable=False)  # المستوى التعليمي (مثال: مبتدئ، متوسط، متقدم)
    grade = Column(String(50), nullable=False)  # الصف الدراسي (مثال: الصف الأول الثانوي)
    number_session = Column(Integer, nullable=False)  # عدد الحصص في الشهر
    total_seats = Column(Integer, nullable=False)  # إجمالي المقاعد
    # remaining_seats = Column(Integer, nullable=False)  # المقاعد المتاحة
    # class_duration = Column(Integer, nullable=False)  # مدة الحصة بالدقائق
    start_date = Column(Date, nullable=False)  # تاريخ البدء
    end_date = Column(Date, nullable=False)  # تاريخ الانتهاء
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

# class Lessons:
#     __tablename__ = "lessons"

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String, nullable=False)  # عنوان الحصة
#     content = Column(String, nullable=False)

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
