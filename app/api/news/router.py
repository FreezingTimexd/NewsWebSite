from fastapi import APIRouter, Depends, HTTPException, Query

from app.api.news.schemas import Article, ArticleCreate, ArticleDeleteResponse
from app.api.news.service import ArticlesService
from app.api.users.dependencies import get_current_user
from app.api.users.schemas import User

posts_router = APIRouter(
    prefix="/news",
    tags=["Новости"]
)


@posts_router.get("", response_model=list[Article])
async def get_articles(
    articles_service: ArticlesService = Depends(ArticlesService),
) -> list[Article]:
    return await articles_service.get_list()


@posts_router.get("/{article_id}", response_model=Article)
async def get_article_by_id(
    article_id: int,
    articles_service: ArticlesService = Depends(ArticlesService),
) -> Article:
    return await articles_service.find_by_id(article_id)


@posts_router.post("", response_model=Article)
async def post_article(
    create_data: ArticleCreate,
    articles_service: ArticlesService = Depends(ArticlesService),
    current_user: User = Depends(get_current_user),
) -> Article:
    if current_user.is_admin:
        return await articles_service.create(create_data)
    else:
        raise HTTPException(status_code=401, detail="Not an admin")


@posts_router.delete("/{article_id}", response_model=ArticleDeleteResponse)
async def delete_article_by_id(
    article_id: int,
    articles_service: ArticlesService = Depends(ArticlesService),
    current_user: User = Depends(get_current_user),
) -> ArticleDeleteResponse:
    if current_user.is_admin:
        return await articles_service.delete_article(article_id)
    else:
        raise HTTPException(status_code=401, detail="Not an admin")
