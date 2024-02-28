from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    content: str
    media_id: int
    author_id: int

    class Config:
        from_attributes = True


class Article(ArticleCreate):
    id: int


class ArticleDeleteResponse(ArticleCreate):
    id: int
