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
    from psycopg2 import pool
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
    
    # Connection Pool (5-20 connections)
    try:
        connection_pool = pool.ThreadedConnectionPool(
            minconn=5,
            maxconn=20,
            **DB_CONFIG
        )
        logging.info(f"🐘 PostgreSQL connection pool created: {result.hostname}/{result.path[1:]}")
    except Exception as e:
        logging.error(f"❌ Failed to create connection pool: {e}")
        connection_pool = None
    
    logging.info(f"🐘 Using PostgreSQL: {result.hostname}/{result.path[1:]}")
else:
    connection_pool = None
    logging.info("📁 Using SQLite (local development)")

class DatabaseConnection:
    """Unified database connection that works with both SQLite and PostgreSQL"""
    
    def __init__(self):
        self.conn = None
        self.is_postgres = USE_POSTGRES
    
    def connect(self):
        """Establish database connection"""
        if self.is_postgres:
            # Use connection pool if available
            if connection_pool:
                try:
                    self.conn = connection_pool.getconn()
                    self.conn.autocommit = False
                    return self.conn
                except Exception as e:
                    logging.error(f"Failed to get connection from pool: {e}")
            # Fallback to direct connection
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.autocommit = False
        else:
            self.conn = sqlite3.connect("data.db", check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            if self.is_postgres and connection_pool:
                # Return connection to pool
                try:
                    connection_pool.putconn(self.conn)
                except Exception as e:
                    logging.error(f"Failed to return connection to pool: {e}")
                    self.conn.close()
            else:
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

class PostgreSQLConnectionWrapper:
    """Wrapper to add execute() method to PostgreSQL connection"""
    def __init__(self, conn):
        self._conn = conn
        self._cursor = None
    
    def execute(self, query, params=None):
        """Execute query using cursor"""
        # Convert SQLite ? placeholders to PostgreSQL %s
        if '?' in query:
            # Count number of ? to ensure we have right number of params
            num_placeholders = query.count('?')
            query = query.replace('?', '%s')
            
            # Ensure params is a tuple
            if params is not None:
                if not isinstance(params, (tuple, list)):
                    params = (params,)
                elif isinstance(params, list):
                    params = tuple(params)
        
        # Convert SQLite AUTOINCREMENT to PostgreSQL SERIAL
        if 'AUTOINCREMENT' in query.upper():
            query = query.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
            query = query.replace('AUTOINCREMENT', '')
        
        self._cursor = self._conn.cursor()
        try:
            if params:
                self._cursor.execute(query, params)
            else:
                self._cursor.execute(query)
        except Exception as e:
            # Log the error with query and params for debugging
            import logging
            logging.error(f"PostgreSQL execute error: {e}")
            logging.error(f"Query: {query}")
            logging.error(f"Params: {params}")
            raise
        return self._cursor
    
    def commit(self):
        return self._conn.commit()
    
    def rollback(self):
        return self._conn.rollback()
    
    def close(self):
        if self._cursor:
            self._cursor.close()
        if connection_pool and self._conn:
            try:
                connection_pool.putconn(self._conn)
            except:
                self._conn.close()
        elif self._conn:
            self._conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        self.close()

def get_db():
    """Get a database connection (for backward compatibility)"""
    if USE_POSTGRES:
        if connection_pool:
            try:
                conn = connection_pool.getconn()
            except:
                conn = psycopg2.connect(**DB_CONFIG)
        else:
            conn = psycopg2.connect(**DB_CONFIG)
        # Wrap to add execute() method
        return PostgreSQLConnectionWrapper(conn)
    else:
        conn = sqlite3.connect("data.db", check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

# Legacy support - keep existing _db_connect function working
def _db_connect():
    """Legacy database connection function"""
    return get_db()
