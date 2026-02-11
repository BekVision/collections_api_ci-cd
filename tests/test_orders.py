from app.models.category import Category
from app.models.product import Product
from app.repositories.product import ProductRepository


def test_create_order_increments_sold_count(client, db_session):
    category = Category(name="Dresses")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    product = Product(
        name="Summer Dress",
        description="Light and comfortable",
        price=120.0,
        rating=4.5,
        category_id=category.id,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    client.post(
        "/auth/register",
        json={"email": "buyer@example.com", "password": "password123", "is_admin": False},
    )
    login_response = client.post(
        "/auth/login",
        data={"username": "buyer@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    order_response = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={"items": [{"product_id": product.id, "quantity": 2}]},
    )
    assert order_response.status_code == 201
    payload = order_response.json()
    assert payload["status"] == "Success"
    assert len(payload["items"]) == 1

    updated_product = ProductRepository(db_session).get(product.id)
    assert updated_product is not None
    assert updated_product.sold_count == 2
