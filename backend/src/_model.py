from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
  full_name: str = Field(..., min_length=3, max_length=50, description="Full name of the user")
  username: str = Field(..., min_length=3, max_length=30, pattern=r'^\w+$', description="Unique username")
  password: str = Field(..., min_length=8, description="Password with at least 8 characters")
  gender: str = Field(..., pattern=r'^(male|female)$', description="Gender must be 'male' or 'female'")
  email: EmailStr = Field(..., description="A valid email address")
  is_teacher: bool = Field(False, description="Is the user a teacher")

  class Config:
    from_attributes = True

class UserCheck(BaseModel):
  email: EmailStr = Field(..., description="A valid email address")
  password: str = Field(..., min_length=8, description="Password with at least 8 characters")

  class Config:
    from_attributes = True
