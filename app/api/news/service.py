from fastapi import Depends
from sqlalchemy import select, insert, delete

from app.api.news.schemas import ArticleCreate, Article, ArticleDeleteResponse
from app.database import get_session, Session
from app import models


class ArticlesService:
    model = models.Article

    def __init__(
        self,
        session: Session = Depends(get_session),
    ) -> None:
        self.session = session

    async def get_list(self) -> list[Article]:
        query = select(self.model)
        async with self.session() as session, session.begin():
            result = await session.scalars(query)
            return [Article.from_orm(row) for row in result.all()]

    async def create(self, data: ArticleCreate) -> Article:
        query = insert(self.model).values(**data.dict()).returning(self.model)
        async with self.session() as session, session.begin():
            article = (await session.execute(query)).scalar_one()
            return Article.from_orm(article)

    async def find_by_id(self, model_id: int) -> Article:
        query = select(self.model).filter_by(id=model_id)
        async with self.session() as session, session.begin():
            return Article.from_orm(await session.scalar(query))

    async def delete_article(self, model_id: int) -> ArticleDeleteResponse:
        query = delete(self.model).where(self.model.id == model_id).returning(self.model)
        async with self.session() as session, session.begin():
            return ArticleDeleteResponse.from_orm((await session.execute(query)).scalar_one())
