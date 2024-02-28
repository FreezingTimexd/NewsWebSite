import json

import pytest
from starlette import status

from app.api.news.schemas import ArticleCreate


@pytest.mark.asyncio
async def test_get_article_ok(
    client,
):
    response = await client.get(
        "/news",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()


@pytest.mark.asyncio
async def test_create_article_ok(client):
    article = ArticleCreate(
        title="test",
        content="test",
        media_id=2,
        author_id=1,
    )
    response = await client.post(
        "/news",
        json=json.loads(article.json()),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()


@pytest.mark.asyncio
async def test_create_article_already_exists(client):
    article = ArticleCreate(
        title="test",
        content="test",
        media_id=2,
        author_id=1,
    )
    response = await client.post(
        "/news",
        json=json.loads(article.json()),
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert (response.json()["Article with this name already exists"]["409"])
