from pydantic import BaseModel, EmailStr, Field
from datetime import date


class UserCreate(BaseModel):
    full_name: str = Field(
        ..., min_length=3, max_length=50, description="Full name of the user"
    )
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern=r"^\w+$",
        description="Unique username",
    )
    password: str = Field(
        ..., min_length=8, description="Password with at least 8 characters"
    )
    gender: str = Field(
        ..., pattern=r"^(male|female)$", description="Gender must be 'male' or 'female'"
    )
    email: EmailStr = Field(..., description="A valid email address")
    is_teacher: bool = Field(False, description="Is the user a teacher")

    class Config:
        from_attributes = True


class UserCheck(BaseModel):
    email: EmailStr = Field(..., description="A valid email address")
    password: str = Field(
        ..., min_length=8, description="Password with at least 8 characters"
    )

    class Config:
        from_attributes = True


class UserDelete(BaseModel):
    token: str = Field(..., min_length=35, max_length=35, description="Set Token")

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    token: str = Field(..., min_length=35, max_length=35, description="Set Token")
    grade: str = Field(..., description="Set Grade")
    level: str = Field(..., description="Set Level")

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    token: str = Field(..., min_length=35, max_length=35, description="Set Token")
    course_name: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., max_length=500)  # وصف الدورة
    lesson_price: float = Field(..., gt=0)         # سعر الحصة بالدولار
    material: str = Field(..., max_length=255)     # المواد التعليمية
    level: str = Field(..., max_length=50)         # المستوى الدراسي
    grade: str = Field(..., max_length=50)         # الصف
    number_session: int = Field(..., gt=0)        # عدد الحصص في الشهر
    total_seats: int = Field(..., ge=1)            # إجمالي المقاعد المتاحة
    remaining_seats: int = Field(..., ge=0)        # المقاعد المتبقية
    class_duration: int = Field(..., gt=0)         # مدة الحصة بالدقائق
    start_date: date = Field(...)                  # تاريخ البدء
    end_date: date = Field(...)                    # تاريخ الانتهاء

    class Config:
        from_attributes = True

# class LessonCreate(BaseModel):
#     title
#     lesson_date
#     preview true | false
#     upload_video