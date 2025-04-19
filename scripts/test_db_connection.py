"""
Test script for database connection.
"""

import sys
from sqlalchemy import create_engine, text

# Add the project root to the Python path
sys.path.append(".")

from config.config import get_config

def test_db_connection():
    """Test database connection."""
    config = get_config()
    db_config = config.database
    
    connection_string = f"postgresql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}"
    
    print(f"Connecting to database: {connection_string}")
    
    try:
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Connection successful!")
            return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_db_connection()
