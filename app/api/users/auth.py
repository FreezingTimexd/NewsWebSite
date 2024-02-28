from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.api.users.service import UserService
from jose import jwt
from pydantic import EmailStr
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


async def auth_user(email: EmailStr, password: str, user_service: UserService):
    user = await user_service.find_one_or_none(email)
    if not user or not verify_password(password, user.password):
        return None
    return user
