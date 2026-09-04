from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routes import tools, news

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Tools Discovery Platform API",
    description="An advanced AI Tools discovery platform with real-time news and notifications",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tools.router)
app.include_router(news.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to AI Tools Discovery Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "tools": "/api/tools",
            "news": "/api/news",
            "api_docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {"status": "ok", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)