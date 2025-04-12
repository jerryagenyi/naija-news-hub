"""
Tests for the WebsiteRepository class.

This module provides tests for the WebsiteRepository class.
"""

import pytest
from sqlalchemy.exc import IntegrityError

from src.database_management.models import Website, Category
from src.database_management.repositories.website_repository import WebsiteRepository

class TestWebsiteRepository:
    """Test cases for WebsiteRepository."""

    def test_create_website(self, website_repository):
        """Test creating a website."""
        # Prepare test data
        website_data = {
            "name": "New Test Website",
            "base_url": "https://newexample.com",
            "description": "A new test website",
            "logo_url": "https://newexample.com/logo.png",
            "sitemap_url": "https://newexample.com/sitemap.xml",
            "active": True
        }

        # Create website
        website = website_repository.create_website(website_data)

        # Verify website was created
        assert website.id is not None
        assert website.name == "New Test Website"
        assert website.base_url == "https://newexample.com"
        assert website.description == "A new test website"
        assert website.active is True

    def test_create_website_duplicate_url(self, website_repository, sample_website):
        """Test creating a website with a duplicate URL."""
        # Prepare test data with the same URL as sample_website
        website_data = {
            "name": "Duplicate URL Website",
            "base_url": sample_website.base_url,  # Same URL as sample_website
            "description": "A duplicate URL website",
            "active": True
        }

        # Attempt to create website with duplicate URL should raise IntegrityError
        with pytest.raises(IntegrityError):
            website_repository.create_website(website_data)

    def test_get_website_by_id(self, website_repository, sample_website):
        """Test getting a website by ID."""
        # Get website by ID
        website = website_repository.get_website_by_id(sample_website.id)

        # Verify website was retrieved
        assert website is not None
        assert website.id == sample_website.id
        assert website.name == sample_website.name
        assert website.base_url == sample_website.base_url

    def test_get_website_by_id_not_found(self, website_repository):
        """Test getting a website by ID that doesn't exist."""
        # Get website by non-existent ID
        website = website_repository.get_website_by_id(999)

        # Verify website was not found
        assert website is None

    def test_get_website_by_url(self, website_repository, sample_website):
        """Test getting a website by URL."""
        # Get website by URL
        website = website_repository.get_website_by_url(sample_website.base_url)

        # Verify website was retrieved
        assert website is not None
        assert website.id == sample_website.id
        assert website.name == sample_website.name
        assert website.base_url == sample_website.base_url

    def test_get_website_by_url_not_found(self, website_repository):
        """Test getting a website by URL that doesn't exist."""
        # Get website by non-existent URL
        website = website_repository.get_website_by_url("https://nonexistent.com")

        # Verify website was not found
        assert website is None

    def test_get_all_websites(self, website_repository, sample_website):
        """Test getting all websites."""
        # Create another website
        website_data = {
            "name": "Another Test Website",
            "base_url": "https://another-example.com",
            "description": "Another test website",
            "active": True
        }
        website_repository.create_website(website_data)

        # Get all websites
        websites = website_repository.get_all_websites()

        # Verify websites were retrieved
        assert len(websites) == 2

    def test_get_all_websites_active_only(self, website_repository, sample_website):
        """Test getting all active websites."""
        # Create an inactive website
        website_data = {
            "name": "Inactive Test Website",
            "base_url": "https://inactive-example.com",
            "description": "An inactive test website",
            "active": False
        }
        website_repository.create_website(website_data)

        # Get all active websites
        websites = website_repository.get_all_websites(active_only=True)

        # Verify only active websites were retrieved
        assert len(websites) == 1
        assert websites[0].active is True

    def test_update_website(self, website_repository, sample_website):
        """Test updating a website."""
        # Prepare update data
        update_data = {
            "name": "Updated Test Website",
            "description": "An updated test website",
            "logo_url": "https://example.com/updated-logo.png"
        }

        # Update website
        updated_website = website_repository.update_website(sample_website.id, update_data)

        # Verify website was updated
        assert updated_website is not None
        assert updated_website.id == sample_website.id
        assert updated_website.name == "Updated Test Website"
        assert updated_website.description == "An updated test website"
        assert updated_website.logo_url == "https://example.com/updated-logo.png"
        assert updated_website.base_url == sample_website.base_url  # URL should not change

    def test_update_website_not_found(self, website_repository):
        """Test updating a website that doesn't exist."""
        # Prepare update data
        update_data = {
            "name": "Updated Test Website",
            "description": "An updated test website"
        }

        # Update non-existent website
        updated_website = website_repository.update_website(999, update_data)

        # Verify website was not found
        assert updated_website is None

    def test_delete_website(self, website_repository, sample_website):
        """Test deleting a website."""
        # Delete website
        result = website_repository.delete_website(sample_website.id)

        # Verify website was deleted
        assert result is True
        assert website_repository.get_website_by_id(sample_website.id) is None

    def test_delete_website_not_found(self, website_repository):
        """Test deleting a website that doesn't exist."""
        # Delete non-existent website
        result = website_repository.delete_website(999)

        # Verify website was not found
        assert result is False

    def test_create_category(self, website_repository, sample_website):
        """Test creating a category."""
        # Prepare category data
        category_data = {
            "name": "New Test Category",
            "url": "https://example.com/new-test-category"
        }

        # Create category
        category = website_repository.create_category(sample_website.id, category_data)

        # Verify category was created
        assert category.id is not None
        assert category.name == "New Test Category"
        assert category.url == "https://example.com/new-test-category"
        assert category.website_id == sample_website.id

    def test_get_category_by_id(self, website_repository, sample_categories):
        """Test getting a category by ID."""
        # Get category by ID
        category = website_repository.get_category_by_id(sample_categories[0].id)

        # Verify category was retrieved
        assert category is not None
        assert category.id == sample_categories[0].id
        assert category.name == sample_categories[0].name
        assert category.url == sample_categories[0].url

    def test_get_category_by_id_not_found(self, website_repository):
        """Test getting a category by ID that doesn't exist."""
        # Get category by non-existent ID
        category = website_repository.get_category_by_id(999)

        # Verify category was not found
        assert category is None

    def test_get_category_by_name(self, website_repository, sample_website, sample_categories):
        """Test getting a category by name."""
        # Get category by name
        category = website_repository.get_category_by_name(sample_website.id, sample_categories[0].name)

        # Verify category was retrieved
        assert category is not None
        assert category.id == sample_categories[0].id
        assert category.name == sample_categories[0].name
        assert category.url == sample_categories[0].url

    def test_get_category_by_name_not_found(self, website_repository, sample_website):
        """Test getting a category by name that doesn't exist."""
        # Get category by non-existent name
        category = website_repository.get_category_by_name(sample_website.id, "Non-existent Category")

        # Verify category was not found
        assert category is None

    def test_get_website_categories(self, website_repository, sample_website, sample_categories):
        """Test getting categories for a website."""
        # Get categories for website
        categories = website_repository.get_website_categories(sample_website.id)

        # Verify categories were retrieved
        assert len(categories) == len(sample_categories)

    def test_create_or_update_category_update(self, website_repository, sample_categories):
        """Test updating a category using create_or_update_category."""
        # Prepare update data
        update_data = {
            "name": "Updated Test Category",
            "url": sample_categories[0].url  # Use the same URL to trigger an update
        }

        # Update category
        updated_category = website_repository.create_or_update_category(
            sample_categories[0].website_id, update_data
        )

        # Verify category was updated
        assert updated_category is not None
        assert updated_category.id == sample_categories[0].id
        assert updated_category.name == "Updated Test Category"
        assert updated_category.url == sample_categories[0].url

    def test_deactivate_category(self, website_repository, sample_categories, db_session):
        """Test deactivating a category (soft delete)."""
        # Get the category
        category = website_repository.get_category_by_id(sample_categories[0].id)

        # Deactivate the category by setting active=False
        update_data = {"active": False}
        db_session.query(Category).filter(Category.id == category.id).update(update_data)
        db_session.commit()

        # Verify category was deactivated
        updated_category = website_repository.get_category_by_id(category.id)
        assert updated_category is not None
        assert updated_category.active is False

        # Verify category is not returned when active_only=True
        categories = website_repository.get_website_categories(category.website_id, active_only=True)
        category_ids = [c.id for c in categories]
        assert category.id not in category_ids

    def test_create_or_update_website_create(self, website_repository):
        """Test creating a website with create_or_update_website."""
        # Prepare test data
        website_data = {
            "name": "New Test Website",
            "base_url": "https://new-example.com",
            "description": "A new test website",
            "active": True
        }

        # Create website
        website = website_repository.create_or_update_website(website_data)

        # Verify website was created
        assert website.id is not None
        assert website.name == "New Test Website"
        assert website.base_url == "https://new-example.com"

    def test_create_or_update_website_update(self, website_repository, sample_website):
        """Test updating a website with create_or_update_website."""
        # Prepare update data
        update_data = {
            "name": "Updated Test Website",
            "base_url": sample_website.base_url,  # Same URL as sample_website
            "description": "An updated test website",
            "active": True
        }

        # Update website
        website = website_repository.create_or_update_website(update_data)

        # Verify website was updated
        assert website.id == sample_website.id
        assert website.name == "Updated Test Website"
        assert website.description == "An updated test website"
