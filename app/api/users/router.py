from fastapi import APIRouter, HTTPException, Depends, Response

from app.api.users.auth import get_password_hash, auth_user, create_access_token
from app.api.users.dependencies import get_current_user, get_current_user_admin
from app.api.users.schemas import User, UserAuth, UserDeleteResponse
from app.api.users.service import UserService

user_router = APIRouter(
    prefix="/auth",
    tags=["Пользователи"],
)


@user_router.post("/register", response_model=UserAuth)
async def register_user(
    user_data: UserAuth,
    user_service: UserService = Depends(UserService),
) -> UserAuth:
    existing_user = await user_service.find_one_or_none(model_email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=409)
    hashed_password = get_password_hash(user_data.password)
    return await user_service.register(user_data, password=hashed_password)


@user_router.post("/login", response_model=User)
async def login_user(
    response: Response,
    user_data: UserAuth,
    user_service: UserService = Depends(UserService),
) -> User:
    user = await auth_user(user_data.email, user_data.password, user_service)
    if not user:
        raise HTTPException(status_code=401)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("website_access_token", access_token, httponly=True)
    return User.from_orm(user)


@user_router.post("/logout", response_model=None)
async def logout(
    response: Response
) -> None:
    response.delete_cookie("averts_access_token")


@user_router.get("/me", response_model=User)
async def read_users_me(
    user: User = Depends(get_current_user)
) -> User:
    return user


@user_router.get("/all", response_model=list[User])
async def get_all_users(
    user: User = Depends(get_current_user_admin),
    user_service: UserService = Depends(UserService)
) -> list[User]:
    if user.is_admin:
        return await user_service.find_all()
    else:
        raise HTTPException(status_code=401, detail="Not an admin")


@user_router.delete("/{user_id}", response_model=UserDeleteResponse)
async def delete_user_by_id(
    user_id: int,
    user_service: UserService = Depends(UserService),
    current_user: User = Depends(get_current_user),
) -> UserDeleteResponse:
    if current_user.is_admin:
        return await user_service.delete_user(user_id)
    else:
        raise HTTPException(status_code=401, detail="Not an admin")
