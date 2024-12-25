# ###################### IMPORT LIBRARY #######################
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pathlib import Path
import os
import uuid

# ###################### IMPORT MODULES #######################
import src.models as models
import src.schemas as schemas
import src.config as config
import src.utiles as utiles
from src.encryption import TPE

# #############################################################

# ###################### INIT ENCRYPTION #######################
tpe = TPE(config.encryption_password)
# ###################### INIT PATHs ##############################
CERTIFICATES_DIR = Path("users/certificates")
CERTIFICATES_DIR.mkdir(exist_ok=True)


class APIV1:
  def __init__(self):
    # ###################### INIT ROUTER #######################
    self.router = APIRouter(prefix="/api/v1")

    @self.router.get("/", response_class=HTMLResponse)
    async def read_root():
      file_path = "./docs/docs.html"
      if not os.path.exists(file_path):
          raise HTTPException(status_code=404, detail="File not found")
      with open(file_path, "r") as html_file:
          html_content = html_file.read()
      return HTMLResponse(content=html_content)


    @self.router.post("/adduser/")
    async def add_user(
      info: schemas.UserCreate, db: AsyncSession = Depends(config.get_db)
    ):
      db_user = await db.execute(
          select(models.User).filter(models.User.username == info.username)
      )
      db_user = db_user.scalars().first()

      db_user_email_check = await db.execute(
        select(models.User).filter(models.User.email == info.email)
      )
      db_user_email_check = db_user_email_check.scalars().first()

      if db_user_email_check:
        raise HTTPException(status_code=400, detail="email already registered")
      if db_user:
        raise HTTPException(status_code=400, detail="Username already used")

      token = await utiles.checkTokenExist(db)

      encryption_password = tpe.encrypt(info.password)

      db_user = models.User(
        full_name=info.full_name,
        username=info.username,
        password=encryption_password,
        gender=info.gender,
        email=info.email,
        token=token,
        is_teacher=info.is_teacher,
      )

      db.add(db_user)
      await db.commit()
      await db.refresh(db_user)
      user_directory = f"./users/{token}"
      try:
        os.makedirs(user_directory, exist_ok=True)
      except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user directory: {str(e)}")
      return db_user

    @self.router.post("/checkuser/")
    async def check_user(
      info: schemas.UserCheck, db: AsyncSession = Depends(config.get_db)
    ):
      db_user = await db.execute(
        select(models.User).filter(models.User.email == info.email)
      )
      db_user = db_user.scalars().first()

      if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

      encrypted_password = db_user.password

      try:
        decrypted_password = tpe.decrypt(encrypted_password)
      except ValueError as e:
        raise HTTPException(status_code=500, detail="Error decrypting password")

      if decrypted_password == info.password:
        return {
          "full_name": db_user.full_name,
          "username": db_user.username,
          "gender": db_user.gender,
          "email": db_user.email,
          "is_teacher": db_user.is_teacher,
          "token": db_user.token,
        }
      else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    @self.router.delete("/deleteuser/")
    async def delete_user(
      info: schemas.UserDelete, db: AsyncSession = Depends(config.get_db)
    ):
      db_user = await db.execute(
        select(models.User).filter(models.User.token == info.token)
      )
      db_user = db_user.scalars().first()
      if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
      await db.delete(db_user)
      await db.commit()

      return {"detail": "User deleted successfully"}

    @self.router.post("/adtchr/")
    async def add_teacher(
      token: str = Form(...),
      subject: str = Form(...),
      certificate: UploadFile = File(...),
      db: AsyncSession = Depends(config.get_db),
    ):
      db_teacher = await db.execute(
        select(models.User).filter(models.User.token == token)
      )
      db_teacher = db_teacher.scalars().first()

      if not db_teacher:
        raise HTTPException(status_code=404, detail="User not found")

      if certificate.content_type != "application/pdf":
        raise HTTPException(
          status_code=400,
          detail="Invalid file type. Only PDF files are allowed.",
        )

      unique_filename = f"{uuid.uuid4()}_certificate_{certificate.filename}"
      file_location = os.path.join("users", "certificates", unique_filename)
      # file_location = CERTIFICATES_DIR / certificate.filename
      try:
        os.makedirs(
          os.path.dirname(file_location), exist_ok=True
        )  # إنشاء المجلدات إذا لم تكن موجودة
        with open(file_location, "wb") as file:
          file.write(await certificate.read())
      except Exception as e:
        raise HTTPException(
          status_code=500, detail=f"Something went wrong: {str(e)}"
        )

      db_teacher = models.Teacher(
        user_id=db_teacher.id,
        study_material=subject,
        certificate=str(file_location),
      )
      db.add(db_teacher)
      await db.commit()

      return {"message": "Certificate uploaded successfully", "subject": subject}

    @self.router.post("/adstudent/")
    async def add_student(
      info: schemas.StudentCreate, db: AsyncSession = Depends(config.get_db)
    ):
      db_user = await db.execute(
        select(models.User).filter(models.User.token == info.token)
      )
      db_user = db_user.scalars().first()

      db_student = models.Student(
        user_id=db_user.id, grade=info.grade, level=info.level
      )

      db.add(db_student)
      await db.commit()
      await db.refresh(db_student)
      return db_student
    
    # ADD COURSES
    @self.router.post("/addcourse")
    async def add_course(
      info: schemas.CourseCreate, db: AsyncSession = Depends(config.get_db)
      ): 
      db_teacher = await db.execute(
        select(models.User).filter(models.User.token == info.token)
      )
      db_teacher = db_teacher.scalars().first()

      if not db_teacher:
        raise HTTPException(status_code=404, detail="User not found")
      if db_teacher.is_teacher == 0:
        raise HTTPException(status_code=404, detail="You cannot create courses because you are a student.")
      
      
      db_course = models.Course(
        course_name=info.course_name,
        description=info.description,
        lesson_price=info.lesson_price,
        material=info.material,
        level=info.level,
        grade=info.grade,
        number_session=info.number_session,
        total_seats=info.total_seats,
        remaining_seats=info.remaining_seats,
        class_duration=info.class_duration,
        start_date=info.start_date,
        end_date=info.end_date,
        teacher_id=db_teacher.id
      )

      db.add(db_course)
      await db.commit()
      await db.refresh(db_course)
      return db_course
    
    # Add Lessons
    @self.router.post("/courses/{course_id}/addlesson")
    async def add_lesson(
      course_id: int,
      info: schemas.CourseCreate, db: AsyncSession = Depends(config.get_db)
    ): ...