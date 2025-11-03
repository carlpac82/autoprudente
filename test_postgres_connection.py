"""
Test PostgreSQL Connection
Run this to verify the database connection works
"""

import os
import sys

def test_connection():
    """Test database connection"""
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL not set")
        print("💡 This is normal for local development (will use SQLite)")
        print("💡 In Render, DATABASE_URL will be set automatically")
        return False
    
    print(f"🔍 Testing PostgreSQL connection...")
    print(f"📍 Host: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'unknown'}")
    
    try:
        from database import get_db_connection, USE_POSTGRES
        
        if not USE_POSTGRES:
            print("❌ PostgreSQL mode not enabled")
            return False
        
        print("✅ PostgreSQL mode enabled")
        
        # Test connection
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Connected successfully!")
            print(f"📊 PostgreSQL version: {version}")
            
            # Test table creation
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_connection (
                    id SERIAL PRIMARY KEY,
                    test_value VARCHAR(255)
                )
            """)
            print("✅ Table creation test passed")
            
            # Test insert
            cursor.execute("INSERT INTO test_connection (test_value) VALUES (%s) RETURNING id", ("test",))
            test_id = cursor.fetchone()[0]
            print(f"✅ Insert test passed (ID: {test_id})")
            
            # Test select
            cursor.execute("SELECT test_value FROM test_connection WHERE id = %s", (test_id,))
            result = cursor.fetchone()[0]
            print(f"✅ Select test passed (Value: {result})")
            
            # Cleanup
            cursor.execute("DROP TABLE test_connection")
            print("✅ Cleanup completed")
            
            conn.commit()
        
        print("\n🎉 All tests passed! PostgreSQL is working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
