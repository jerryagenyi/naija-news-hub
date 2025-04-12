"""
Main API module for Naija News Hub.

This module provides the FastAPI application for the API.
"""

import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from config.config import get_config
from src.database_management.connection import get_db, init_db
from src.api_endpoints.routes import websites, articles, scraping, categories

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Naija News Hub API",
    description="API for Nigerian News Aggregation & Analysis Platform",
    version="0.1.0",
)

# Add CORS middleware
config = get_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(websites.router, prefix="/api/websites", tags=["websites"])
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(scraping.router, prefix="/api/scraping", tags=["scraping"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])

@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup."""
    logger.info("Initializing database")
    init_db()

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
