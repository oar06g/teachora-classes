from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import src.models as models
import src._model as _model
import src.config as config
import src.utiles as utiles
from src.encryption import TPE

tpe = TPE(config.encryption_password)

class APIV1:
  def __init__(self):
    self.router = APIRouter(prefix="/api/v1")

    @self.router.get("/")
    async def read_root():
      return {"Hello": "World"}

    @self.router.post("/adduser/")
    async def add_user(
      info: _model.UserCreate, db: AsyncSession = Depends(config.get_db)
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
        raise HTTPException(
          status_code=400, detail="Username already registered"
      )

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
      return db_user
    
    @self.router.post("/checkuser/")
    async def check_user(info: _model.UserCheck, db: AsyncSession = Depends(config.get_db)):
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
        # return {"message": "Login successful", "user": {"email": db_user.email, "username": db_user.username}}
        return {
          "full_name": db_user.full_name,
          "username": db_user.username,
          "gender": db_user.gender,
          "email": db_user.email,
          "is_teacher": db_user.is_teacher,
          "token": db_user.token
        }
      else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
