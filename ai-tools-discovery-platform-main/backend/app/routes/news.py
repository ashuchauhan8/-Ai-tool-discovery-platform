from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import News
from ..schemas import News as NewsSchema

router = APIRouter(prefix="/api/news", tags=["news"])

@router.get("/", response_model=list[NewsSchema])
def get_latest_news(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Get latest AI news"""
    news = db.query(News).order_by(News.published_at.desc()).offset(skip).limit(limit).all()
    return news

@router.get("/{news_id}", response_model=NewsSchema)
def get_news(news_id: int, db: Session = Depends(get_db)):
    """Get a specific news item"""
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        return {"error": "News not found"}
    return news

@router.get("/category/{category}", response_model=list[NewsSchema])
def get_news_by_category(category: str, db: Session = Depends(get_db)):
    """Get news by category"""
    news = db.query(News).filter(News.source == category).all()
    return news