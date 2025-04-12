"""
Tests for the API module.

This module provides tests for the API functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database_management.models import Base
from src.database_management.connection import get_db
from src.api_endpoints.main import app

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)

# Override the get_db dependency
def override_get_db():
    """Get a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create a test client
client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_website():
    """Test creating a website."""
    response = client.post(
        "/api/websites/",
        json={
            "name": "Test Website",
            "base_url": "https://example.com",
            "description": "A test website",
            "active": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Website"
    assert data["base_url"] == "https://example.com"
    assert data["description"] == "A test website"
    assert data["active"] is True
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_websites():
    """Test getting all websites."""
    response = client.get("/api/websites/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_website():
    """Test getting a website by ID."""
    # First, create a website
    create_response = client.post(
        "/api/websites/",
        json={
            "name": "Another Test Website",
            "base_url": "https://another-example.com",
            "description": "Another test website",
            "active": True,
        },
    )
    website_id = create_response.json()["id"]
    
    # Then, get the website
    response = client.get(f"/api/websites/{website_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == website_id
    assert data["name"] == "Another Test Website"
    assert data["base_url"] == "https://another-example.com"

def test_update_website():
    """Test updating a website."""
    # First, create a website
    create_response = client.post(
        "/api/websites/",
        json={
            "name": "Website to Update",
            "base_url": "https://update-example.com",
            "description": "A website to update",
            "active": True,
        },
    )
    website_id = create_response.json()["id"]
    
    # Then, update the website
    response = client.put(
        f"/api/websites/{website_id}",
        json={
            "name": "Updated Website",
            "description": "An updated website",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == website_id
    assert data["name"] == "Updated Website"
    assert data["description"] == "An updated website"
    assert data["base_url"] == "https://update-example.com"  # Unchanged

def test_delete_website():
    """Test deleting a website."""
    # First, create a website
    create_response = client.post(
        "/api/websites/",
        json={
            "name": "Website to Delete",
            "base_url": "https://delete-example.com",
            "description": "A website to delete",
            "active": True,
        },
    )
    website_id = create_response.json()["id"]
    
    # Then, delete the website
    response = client.delete(f"/api/websites/{website_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Website deleted successfully"}
    
    # Verify that the website is deleted
    get_response = client.get(f"/api/websites/{website_id}")
    assert get_response.status_code == 404
