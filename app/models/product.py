from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(String(1000))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    rating: Mapped[float] = mapped_column(Float, default=0)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    views_count: Mapped[int] = mapped_column(Integer, default=0)
    sold_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    category = relationship("Category", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product")
    # feedback
    ratings = relationship("ProductRating", back_populates="product", cascade="all, delete-orphan")
    comments = relationship("ProductComment", back_populates="product", cascade="all, delete-orphan")


class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product = relationship("Product", back_populates="images")


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product = relationship("Product", back_populates="variants")
