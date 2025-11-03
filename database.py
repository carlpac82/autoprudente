"""
Database Connection Manager
Supports both SQLite (local development) and PostgreSQL (production)
"""

import os
import sqlite3
from typing import Optional
from contextlib import contextmanager
import logging

# Check if we're in production (Render) or local development
DATABASE_URL = os.getenv("DATABASE_URL")  # Render PostgreSQL URL

# Fix for Render environment variable issue
if not DATABASE_URL:
    # Try to extract from printenv output (Render stores it as Key/Value)
    try:
        import subprocess
        result = subprocess.run(['printenv'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if line.startswith('Value=postgresql://'):
                DATABASE_URL = line.split('=', 1)[1]
                os.environ['DATABASE_URL'] = DATABASE_URL
                logging.info(f"✅ Extracted DATABASE_URL from environment")
                break
    except Exception as e:
        logging.warning(f"Could not extract DATABASE_URL: {e}")

USE_POSTGRES = DATABASE_URL is not None

if USE_POSTGRES:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from urllib.parse import urlparse
    
    # Parse DATABASE_URL
    result = urlparse(DATABASE_URL)
    DB_CONFIG = {
        'host': result.hostname,
        'port': result.port,
        'database': result.path[1:],
        'user': result.username,
        'password': result.password,
        'sslmode': 'require'
    }
    logging.info(f"🐘 Using PostgreSQL: {result.hostname}/{result.path[1:]}")
else:
    logging.info("📁 Using SQLite (local development)")

class DatabaseConnection:
    """Unified database connection that works with both SQLite and PostgreSQL"""
    
    def __init__(self):
        self.conn = None
        self.is_postgres = USE_POSTGRES
    
    def connect(self):
        """Establish database connection"""
        if self.is_postgres:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.autocommit = False
        else:
            self.conn = sqlite3.connect("data.db", check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def execute(self, query: str, params: tuple = None):
        """Execute a query with automatic dialect conversion"""
        if not self.conn:
            self.connect()
        
        # Convert SQLite syntax to PostgreSQL if needed
        if self.is_postgres:
            query = self._convert_to_postgres(query)
        
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor
    
    def commit(self):
        """Commit transaction"""
        if self.conn:
            self.conn.commit()
    
    def rollback(self):
        """Rollback transaction"""
        if self.conn:
            self.conn.rollback()
    
    def _convert_to_postgres(self, query: str) -> str:
        """Convert SQLite-specific syntax to PostgreSQL"""
        # AUTOINCREMENT -> SERIAL
        query = query.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "SERIAL PRIMARY KEY")
        query = query.replace("AUTOINCREMENT", "")
        
        # TEXT -> VARCHAR/TEXT (PostgreSQL is more strict)
        # Keep TEXT as is, it works in PostgreSQL
        
        # REAL -> DOUBLE PRECISION
        query = query.replace("REAL", "DOUBLE PRECISION")
        
        # BLOB -> BYTEA
        query = query.replace("BLOB", "BYTEA")
        
        # CURRENT_TIMESTAMP works in both
        
        # IF NOT EXISTS works in both
        
        return query

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    db = DatabaseConnection()
    try:
        conn = db.connect()
        yield conn
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Database error: {e}")
        raise
    finally:
        db.close()

def get_db():
    """Get a database connection (for backward compatibility)"""
    if USE_POSTGRES:
        return psycopg2.connect(**DB_CONFIG)
    else:
        conn = sqlite3.connect("data.db", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

# Legacy support - keep existing _db_connect function working
def _db_connect():
    """Legacy database connection function"""
    return get_db()
