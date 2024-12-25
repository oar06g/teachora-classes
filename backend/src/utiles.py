from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
import src.models as models
import secrets
from sqlalchemy.future import select


def generateTokens(length: int = 35) -> str:
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    token = ""
    for i in range(length):
        random_index = secrets.randbelow(len(characters))
        token += characters[random_index]
    return token


async def checkTokenExist(db: AsyncSession) -> str:
    randomToken = generateTokens()
    try:
        result = await db.execute(
            select(models.User).filter(models.User.token == randomToken)
        )
        user = result.scalars().first()

        if user:
            print("Token exists, generating new one...")
            return await checkTokenExist(db)
        else:
            print("Token does not exist, returning token.")
            return randomToken
    except SQLAlchemyError as e:
        print(f"Error checking token existence: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Database error while checking token"
        )
