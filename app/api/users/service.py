from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select, insert, delete

from app import models
from app.api.users.schemas import User, UserAuth, UserDeleteResponse
from app.database import get_session, Session


class UserService:
    model = models.User

    def __init__(
        self,
        session: Session = Depends(get_session),
    ) -> None:
        self.session = session

    async def find_one_or_none(self, model_email: EmailStr) -> User | None:
        query = select(self.model).filter_by(email=model_email)
        async with self.session() as session, session.begin():
            if user := await session.scalar(query):
                return User.from_orm(user)
            return None

    async def register(self, data: UserAuth, password: str) -> UserAuth:
        query = insert(self.model).values(**data.dict(exclude={"password"}),
                                          password=password).returning(self.model)
        async with self.session() as session, session.begin():
            user = (await session.execute(query)).scalar_one()
            return UserAuth.from_orm(user)

    async def find_by_id(self, model_id: int) -> User:
        query = select(self.model).filter_by(id=model_id)
        async with self.session() as session, session.begin():
            return User.from_orm(await session.scalar(query))

    async def find_all(self) -> list[User]:
        query = select(self.model)
        async with self.session() as session, session.begin():
            result = await session.scalars(query)
            return [User.from_orm(row) for row in result.all()]

    async def delete_user(self, model_id: int) -> UserDeleteResponse:
        query = delete(self.model).where(self.model.id == model_id).returning(self.model)
        async with self.session() as session, session.begin():
            return UserDeleteResponse.from_orm((await session.execute(query)).scalar_one())
