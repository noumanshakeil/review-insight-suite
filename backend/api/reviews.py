from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import reviews as svc

class ReviewIn(BaseModel):
    product: str = Field(min_length=1)
    text: str = Field(min_length=3)
    rating: float = 3.0

router = APIRouter()

@router.get("/reviews")
async def reviews(product: str | None = None, db: AsyncSession = Depends(get_db)):
    rows = await svc.list_reviews(db, product)
    return {"reviews": [{"id": r.id, "product": r.product, "rating": r.rating, "sentiment": r.sentiment, "theme": r.theme, "text": r.text[:160]} for r in rows]}

@router.post("/reviews")
async def create(payload: ReviewIn, db: AsyncSession = Depends(get_db)):
    r = await svc.add_review(db, payload.product, payload.text, payload.rating)
    return {"id": r.id, "theme": r.theme, "sentiment": r.sentiment}

@router.get("/insights")
async def insights(product: str | None = Query(None), db: AsyncSession = Depends(get_db)):
    return await svc.insights(db, product)
