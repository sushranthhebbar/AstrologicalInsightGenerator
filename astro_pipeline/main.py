from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Astrological Insight Generator",
    description="A modular RAG-based astrology service.",
    version="1.0.0"
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
