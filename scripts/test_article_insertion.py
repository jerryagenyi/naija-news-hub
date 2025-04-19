#!/usr/bin/env python
"""
Script to test article insertion with the new schema.
"""
import os
import json
import datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_article_insertion():
    """Test inserting an article with the new schema."""
    # Get database connection details from environment variables
    db_user = os.getenv("DB_USER", "jeremiah")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "naija_news_hub")

    # Create database URL
    if db_password:
        db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    else:
        db_url = f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}"

    # Create engine
    engine = create_engine(db_url)

    try:
        with engine.connect() as connection:
            # Generate a unique timestamp for the URL
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            article_url = f"https://blueprint.ng/test-article-{timestamp}"

            # Create test article
            article_metadata = {
                "content": {
                    "markdown": "# Test Article\n\nThis is a test article for the new schema.\n\n## Section 1\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit.\n\n## Section 2\n\nSed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
                    "word_count": 35,
                    "reading_time": 1
                },
                "metadata": {
                    "title": "Test Article",
                    "author": "Test Author",
                    "published_date": datetime.datetime.now().isoformat(),
                    "source_website": "Blueprint News",
                    "source_url": article_url,
                    "image_url": f"https://blueprint.ng/images/test-article-{timestamp}.jpg",
                    "categories": [
                        {"name": "Politics", "url": "https://blueprint.ng/category/politics"},
                        {"name": "Business", "url": "https://blueprint.ng/category/business"}
                    ]
                }
            }

            tags = [
                {"name": "Test", "url": "https://blueprint.ng/tag/test"},
                {"name": "Example", "url": "https://blueprint.ng/tag/example"}
            ]

            # Insert article
            result = connection.execute(
                text("""
                    INSERT INTO articles
                    (title, url, author, published_at, image_url, website_id, article_metadata, tags, last_checked_at)
                    VALUES (:title, :url, :author, :published_at, :image_url, :website_id, :article_metadata, :tags, :last_checked_at)
                    RETURNING id
                """),
                {
                    "title": "Test Article",
                    "url": article_url,
                    "author": "Test Author",
                    "published_at": datetime.datetime.now(),
                    "image_url": f"https://blueprint.ng/images/test-article-{timestamp}.jpg",
                    "website_id": 1,
                    "article_metadata": json.dumps(article_metadata),
                    "tags": json.dumps(tags),
                    "last_checked_at": datetime.datetime.now()
                }
            )
            article_id = result.scalar()
            connection.commit()

            print(f"Inserted article with ID: {article_id}")

            # Link article to categories
            for category_id in [1, 2]:  # Politics and Business
                connection.execute(
                    text("""
                        INSERT INTO article_categories (article_id, category_id)
                        VALUES (:article_id, :category_id)
                    """),
                    {"article_id": article_id, "category_id": category_id}
                )
            connection.commit()

            print("Linked article to categories")

            # Retrieve article
            result = connection.execute(
                text("""
                    SELECT a.*,
                           array_agg(c.name) as category_names
                    FROM articles a
                    LEFT JOIN article_categories ac ON a.id = ac.article_id
                    LEFT JOIN categories c ON ac.category_id = c.id
                    WHERE a.id = :article_id
                    GROUP BY a.id
                """),
                {"article_id": article_id}
            )
            article = result.mappings().one()

            print("\nRetrieved article:")
            print(f"  - ID: {article['id']}")
            print(f"  - Title: {article['title']}")
            print(f"  - Author: {article['author']}")
            print(f"  - Categories: {article['category_names']}")
            print(f"  - Tags: {article['tags']}")

            # Extract content from JSON
            metadata = article['article_metadata']
            if isinstance(metadata, str):
                metadata = json.loads(metadata)
            content = metadata['content']['markdown']
            print(f"\nContent preview: {content[:100]}...")

            # Test querying with GIN index
            result = connection.execute(
                text("""
                    SELECT id, title
                    FROM articles
                    WHERE article_metadata->'metadata'->'categories' @> '[{"name": "Politics"}]'
                """)
            )
            politics_articles = result.mappings().all()

            print("\nArticles in Politics category:")
            for a in politics_articles:
                print(f"  - {a['id']}: {a['title']}")

        return True
    except Exception as e:
        print(f"Error testing article insertion: {e}")
        return False

if __name__ == "__main__":
    test_article_insertion()
