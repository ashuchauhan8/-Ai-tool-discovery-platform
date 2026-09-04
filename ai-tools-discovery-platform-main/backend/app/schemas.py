from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class AIToolBase(BaseModel):
    name: str
    description: str
    category: str
    url: str
    rating: float = 0.0
    downloads: int = 0
    is_trending: bool = False
    image_url: Optional[str] = None

class AIToolCreate(AIToolBase):
    pass

class AITool(AIToolBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    fullname: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class NewsBase(BaseModel):
    title: str
    description: str
    url: str
    source: str
    image_url: Optional[str] = None
    published_at: datetime

class News(NewsBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserFavoriteBase(BaseModel):
    user_id: int
    tool_id: int

class UserFavorite(UserFavoriteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True