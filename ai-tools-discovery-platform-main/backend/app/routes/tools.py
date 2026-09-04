from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import AITool
from ..schemas import AITool as AIToolSchema, AIToolCreate

router = APIRouter(prefix="/api/tools", tags=["tools"])

@router.get("/", response_model=list[AIToolSchema])
def get_all_tools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all AI tools with pagination"""
    tools = db.query(AITool).offset(skip).limit(limit).all()
    return tools

@router.get("/trending", response_model=list[AIToolSchema])
def get_trending_tools(limit: int = 10, db: Session = Depends(get_db)):
    """Get trending AI tools"""
    tools = db.query(AITool).filter(AITool.is_trending == True).limit(limit).all()
    return tools

@router.get("/search", response_model=list[AIToolSchema])
def search_tools(q: str = Query(...), db: Session = Depends(get_db)):
    """Search AI tools by name or description"""
    tools = db.query(AITool).filter(
        (AITool.name.ilike(f"%{q}%")) | 
        (AITool.description.ilike(f"%{q}%"))
    ).all()
    return tools

@router.get("/category/{category}", response_model=list[AIToolSchema])
def get_tools_by_category(category: str, db: Session = Depends(get_db)):
    """Get tools by category"""
    tools = db.query(AITool).filter(AITool.category == category).all()
    return tools

@router.get("/{tool_id}", response_model=AIToolSchema)
def get_tool(tool_id: int, db: Session = Depends(get_db)):
    """Get a specific tool by ID"""
    tool = db.query(AITool).filter(AITool.id == tool_id).first()
    if not tool:
        return {"error": "Tool not found"}
    return tool

@router.post("/", response_model=AIToolSchema)
def create_tool(tool: AIToolCreate, db: Session = Depends(get_db)):
    """Create a new AI tool (Admin only)"""
    db_tool = AITool(**tool.dict())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool