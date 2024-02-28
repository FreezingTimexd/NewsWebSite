from pydantic import EmailStr, BaseModel


class UserAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class User(UserAuth):
    id: int
    username: str | None
    is_admin: bool


class UserDeleteResponse(UserAuth):
    id: int

