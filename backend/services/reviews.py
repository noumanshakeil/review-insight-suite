from __future__ import annotations
import uuid
from collections import Counter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import Review

THEMES = {
    "pricing": ["price", "expensive", "cheap", "cost"],
    "support": ["support", "help", "response"],
    "ux": ["ui", "ux", "design", "confusing", "easy"],
    "reliability": ["crash", "bug", "slow", "uptime"],
}

def theme_of(text: str) -> str:
    low = text.lower()
    for theme, cues in THEMES.items():
        if any(c in low for c in cues):
            return theme
    return "general"

def sentiment_of(text: str, rating: float) -> str:
    if rating >= 4: return "positive"
    if rating <= 2: return "negative"
    low = text.lower()
    if any(w in low for w in ("love", "great", "awesome")): return "positive"
    if any(w in low for w in ("hate", "terrible", "awful")): return "negative"
    return "neutral"

async def add_review(session: AsyncSession, product: str, text: str, rating: float = 3.0) -> Review:
    row = Review(id=uuid.uuid4().hex[:10], product=product[:120], text=text.strip(), rating=float(rating),
                 sentiment=sentiment_of(text, rating), theme=theme_of(text))
    session.add(row); await session.commit(); await session.refresh(row); return row

async def list_reviews(session: AsyncSession, product: str | None = None) -> list[Review]:
    stmt = select(Review)
    if product: stmt = stmt.where(Review.product == product)
    return list((await session.execute(stmt.order_by(Review.created_at.desc()))).scalars())

async def insights(session: AsyncSession, product: str | None = None) -> dict:
    rows = await list_reviews(session, product)
    themes = Counter(r.theme for r in rows)
    sentiments = Counter(r.sentiment for r in rows)
    llm = get_llm()
    sample = "\n".join(r.text for r in rows[:8]) or "(no reviews)"
    narrative = await llm.complete(f"Summarize product review themes:\n{sample}", system="Product insights analyst.")
    return {"themes": dict(themes), "sentiments": dict(sentiments), "narrative": narrative, "count": len(rows)}
