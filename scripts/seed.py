from __future__ import annotations

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.category import Category
from app.models.product import Product, ProductImage
from app.models.user import User


def get_or_create_category(db, name: str) -> Category:
    category = db.scalar(select(Category).where(Category.name == name))
    if category:
        return category
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_or_create_user(db, email: str, password: str, is_admin: bool) -> User:
    user = db.scalar(select(User).where(User.email == email))
    if user:
        if is_admin and not user.is_admin:
            user.is_admin = True
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    user = User(
        email=email,
        hashed_password=hash_password(password),
        is_admin=is_admin,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def upsert_product(
    db,
    name: str,
    description: str,
    price: float,
    rating: float,
    category_id: int,
    images: list[str],
    views: int = 0,
    sold: int = 0,
) -> Product:
    product = db.scalar(select(Product).where(Product.name == name))
    if not product:
        product = Product(
            name=name,
            description=description,
            price=price,
            rating=rating,
            category_id=category_id,
            views_count=views,
            sold_count=sold,
        )
        db.add(product)
        db.commit()
        db.refresh(product)
    else:
        product.description = description
        product.price = price
        product.rating = rating
        product.category_id = category_id
        product.views_count = views
        product.sold_count = sold
        db.add(product)
        db.commit()
        db.refresh(product)

    if images:
        product.images = [ProductImage(url=url) for url in images]
        db.add(product)
        db.commit()
        db.refresh(product)

    return product


def main() -> None:
    db = SessionLocal()
    try:
        get_or_create_user(
            db,
            email="axmedovmaxmud839@gmail.com",
            password="kuchliparol",
            is_admin=True,
        )

        dresses = get_or_create_category(db, "Dresses")
        casual = get_or_create_category(db, "Casual")
        outerwear = get_or_create_category(db, "Outerwear")
        accessories = get_or_create_category(db, "Accessories")

        upsert_product(
            db,
            name="Silk Evening Dress",
            description="Elegant satin finish with soft drape for evening wear.",
            price=420000,
            rating=4.8,
            category_id=dresses.id,
            images=["https://images.unsplash.com/photo-1521572163474-6864f9cf17ab"],
            views=120,
            sold=18,
        )
        upsert_product(
            db,
            name="Linen Summer Set",
            description="Breathable linen co-ord in a warm sand tone.",
            price=280000,
            rating=4.6,
            category_id=casual.id,
            images=["https://images.unsplash.com/photo-1483985988355-763728e1935b"],
            views=95,
            sold=22,
        )
        upsert_product(
            db,
            name="Signature Trench",
            description="Structured trench with minimalist tailoring.",
            price=650000,
            rating=4.9,
            category_id=outerwear.id,
            images=["https://images.unsplash.com/photo-1524504388940-b1c1722653e1"],
            views=160,
            sold=30,
        )
        upsert_product(
            db,
            name="Pearl Accent Blouse",
            description="Soft blouse with pearl button detailing.",
            price=190000,
            rating=4.4,
            category_id=casual.id,
            images=["https://images.unsplash.com/photo-1524504388940-b1c1722653e1"],
            views=70,
            sold=10,
        )
        upsert_product(
            db,
            name="Gold Chain Bag",
            description="Compact evening bag with gold chain strap.",
            price=160000,
            rating=4.3,
            category_id=accessories.id,
            images=["https://images.unsplash.com/photo-1524504388940-b1c1722653e1"],
            views=110,
            sold=14,
        )
        upsert_product(
            db,
            name="Velvet Wrap Dress",
            description="Deep velvet texture with adjustable wrap tie.",
            price=390000,
            rating=4.7,
            category_id=dresses.id,
            images=["https://images.unsplash.com/photo-1483985988355-763728e1935b"],
            views=135,
            sold=20,
        )

        print("Seed completed.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
