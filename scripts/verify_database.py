#!/usr/bin/env python
"""
Script to verify the database schema.
"""
import os
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_database():
    """Verify the database schema."""
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
        # Check tables
        with engine.connect() as connection:
            # Get list of tables
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            print("Tables in database:")
            for table in tables:
                print(f"  - {table}")
            
            # Check articles table structure
            result = connection.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'articles'
                ORDER BY ordinal_position
            """))
            columns = [(row[0], row[1]) for row in result]
            print("\nArticles table structure:")
            for column, data_type in columns:
                print(f"  - {column}: {data_type}")
            
            # Check test data
            result = connection.execute(text("SELECT COUNT(*) FROM websites"))
            website_count = result.scalar()
            
            result = connection.execute(text("SELECT COUNT(*) FROM categories"))
            category_count = result.scalar()
            
            print(f"\nTest data: {website_count} websites, {category_count} categories")
            
            # Check indexes
            result = connection.execute(text("""
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE tablename = 'articles'
                ORDER BY indexname
            """))
            indexes = [(row[0], row[1]) for row in result]
            print("\nIndexes on articles table:")
            for name, definition in indexes:
                print(f"  - {name}: {definition}")
            
        return True
    except Exception as e:
        print(f"Error verifying database: {e}")
        return False

if __name__ == "__main__":
    verify_database()
