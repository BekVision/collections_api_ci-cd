from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.product import ProductRead
from app.services.recommendation import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/most-viewed", response_model=list[ProductRead])
def most_viewed(limit: int = 10, db: Session = Depends(get_db)):
    return RecommendationService(db).most_viewed(limit)


@router.get("/most-sold", response_model=list[ProductRead])
def most_sold(limit: int = 10, db: Session = Depends(get_db)):
    return RecommendationService(db).most_sold(limit)
