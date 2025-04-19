#!/usr/bin/env python
"""
Script to reset the database with the new schema.
"""
import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def reset_database():
    """Reset the database with the new schema."""
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
        # Read SQL script
        with open("migrations/reset_database.sql", "r") as f:
            sql_script = f.read()
        
        # Execute SQL script
        with engine.connect() as connection:
            connection.execute(text(sql_script))
            connection.commit()
        
        print("Database reset complete.")
        return True
    except Exception as e:
        print(f"Error resetting database: {e}")
        return False

if __name__ == "__main__":
    success = reset_database()
    sys.exit(0 if success else 1)
