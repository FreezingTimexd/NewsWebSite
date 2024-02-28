from fastapi import FastAPI

from app.api.news.router import posts_router
from app.api.users.router import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(posts_router)
