import pytest
from httpx import AsyncClient
from fastapi import status
from src.main import app


@pytest.mark.asyncio
async def test_list_collections():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/collections")
    assert response.status_code == status.HTTP_200_OK
    assert "collections" in response.json()


@pytest.mark.asyncio
async def test_list_documents_empty_collection():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/collection/non_existent_collection")
    # Pode ser 200 com lista vazia, ou erro dependendo da sua lógica
    assert response.status_code in (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND)


@pytest.mark.asyncio
async def test_delete_document_invalid_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/collection/test/invalid_id")
    assert response.status_code in (status.HTTP_400_BAD_REQUEST, status.HTTP_500_INTERNAL_SERVER_ERROR)
