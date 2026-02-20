from app.models.category import Category
from app.models.product import Product
from app.repositories.product import ProductRepository


def test_create_order_increments_sold_count(client, db_session):
    # 1) Prepare category + product with stock
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
        stock_count=10,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    # 2) Register buyer and login
    client.post(
        "/auth/register",
        json={"email": "buyer@example.com", "password": "password123", "is_admin": False},
    )
    login_response = client.post(
        "/auth/login",
        data={"username": "buyer@example.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    # 3) Create order -> should be pending
    order_response = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "items": [{"product_id": product.id, "quantity": 2}],
            "delivery_address_text": "Test address",
        },
    )

    assert order_response.status_code == 201
    payload = order_response.json()
    assert payload["status"] in ("pending", "Pending")
    assert len(payload["items"]) == 1

    order_id = payload["id"]

    # 4) Register admin and login (to update status)
    client.post(
        "/auth/register",
        json={"email": "admin@example.com", "password": "password123", "is_admin": True},
    )
    admin_login_response = client.post(
        "/auth/login",
        data={"username": "admin@example.com", "password": "password123"},
    )
    admin_token = admin_login_response.json()["access_token"]

    # 5) Update order status -> delivered (bajarildi)
    status_response = client.put(
        f"/orders/{order_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "delivered"},
    )

    assert status_response.status_code == 200
    updated_payload = status_response.json()
    assert updated_payload["status"] in ("delivered", "Delivered")

    # 6) Now sold_count should be incremented
    updated_product = ProductRepository(db_session).get(product.id)
    assert updated_product is not None
    assert updated_product.sold_count == 2