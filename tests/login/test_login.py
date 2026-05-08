import pytest
from httpx import AsyncClient, ASGITransport

from conf_test_db import app


@pytest.mark.asyncio
async def test_login_email():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.post("/login", data={'username': 'sadauchi1267@gmail.com', 'password': 'Sadauchi98764'})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_login_phone():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.post("/login", data={'username': '+79999999999', 'password': 'Sadauchi98764'})
    assert response.status_code == 200
