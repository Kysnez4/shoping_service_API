import pytest
from httpx import AsyncClient, ASGITransport

from app.auth.jwt import create_access_token
from conf_test_db import app
from tests.shared.info import category_info, product_info


@pytest.mark.asyncio
async def test_new_product_admin():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        user_access_token = create_access_token({"sub": "sadauchi1267@gmail.com"})
        category_obj = await category_info()
        payload = {
            "name": "Quaker Oats",
            "quantity": 4,
            "description": "Quaker: Good Quality Oats",
            "price": 10,
            "category_id": category_obj.id
        }

        response = await ac.post("/products/", json=payload,
                                 headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 201
    assert response.json()['name'] == "Quaker Oats"
    assert response.json()['quantity'] == 4
    assert response.json()['description'] == "Quaker: Good Quality Oats"
    assert response.json()['price'] == 10


@pytest.mark.asyncio
async def test_list_products():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        user_access_token = create_access_token({"sub": "sadauchi1267@gmail.com"})
        category_obj = await category_info()
        await product_info(category_obj)

        response = await ac.get("/products/",
                                headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 200
    assert 'name' in response.json()[0]
    assert 'quantity' in response.json()[0]
    assert 'description' in response.json()[0]
    assert 'price' in response.json()[0]
