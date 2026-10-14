from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.services import reviews as svc

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, product: str = "app", db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Review Insight Suite",
        "product": product, "reviews": await svc.list_reviews(db, product), "insights": await svc.insights(db, product)})

@router.post("/ui/reviews")
async def ui_r(product: str = Form(...), text: str = Form(...), rating: float = Form(3), db: AsyncSession = Depends(get_db)):
    await svc.add_review(db, product, text, rating); return RedirectResponse(f"/?product={product}", status_code=303)
