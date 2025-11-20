#!/usr/bin/env python3
"""
Script to clean up duplicate automated search history entries.

Keeps only the most recent version of each search per day,
deleting older duplicates.
"""

import os
import sys

def cleanup_duplicates():
    """Remove duplicate automated search history entries"""
    
    # Get DATABASE_URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable not set")
        sys.exit(1)
    
    print("🔧 Cleaning up duplicate automated search entries...")
    print(f"📊 Database: {database_url[:30]}...")
    
    try:
        import psycopg2
        
        # Connect to database
        conn = psycopg2.connect(database_url, sslmode='require')
        
        with conn.cursor() as cur:
            # Get statistics before cleanup
            cur.execute("SELECT COUNT(*) FROM automated_search_history")
            total_before = cur.fetchone()[0]
            print(f"\n📊 Total entries before cleanup: {total_before}")
            
            # Find duplicates (same location, pickup_date, search_type on same day)
            cur.execute("""
                WITH duplicates AS (
                    SELECT 
                        location,
                        search_type,
                        pickup_date,
                        DATE(search_date) as search_day,
                        COUNT(*) as count,
                        ARRAY_AGG(id ORDER BY search_date DESC) as ids
                    FROM automated_search_history
                    GROUP BY location, search_type, pickup_date, DATE(search_date)
                    HAVING COUNT(*) > 1
                )
                SELECT 
                    location,
                    search_type,
                    pickup_date,
                    search_day,
                    count,
                    ids
                FROM duplicates
                ORDER BY count DESC, search_day DESC
            """)
            
            duplicates = cur.fetchall()
            
            if not duplicates:
                print("✅ No duplicates found!")
                conn.close()
                return
            
            print(f"\n🔍 Found {len(duplicates)} groups with duplicates:")
            
            total_to_delete = 0
            for location, search_type, pickup_date, search_day, count, ids in duplicates[:10]:
                print(f"  • {location} | {pickup_date} | {search_type} | {search_day}: {count} versions")
                total_to_delete += (count - 1)
            
            if len(duplicates) > 10:
                print(f"  ... and {len(duplicates) - 10} more groups")
            
            print(f"\n⚠️  Total entries to delete: {total_to_delete}")
            
            # Ask for confirmation
            response = input("\n❓ Proceed with cleanup? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Cleanup cancelled")
                conn.close()
                return
            
            # Delete duplicates (keep most recent)
            deleted_count = 0
            for location, search_type, pickup_date, search_day, count, ids in duplicates:
                # Keep the first ID (most recent), delete the rest
                keep_id = ids[0]
                delete_ids = ids[1:]
                
                cur.execute("""
                    DELETE FROM automated_search_history
                    WHERE id = ANY(%s)
                """, (delete_ids,))
                
                deleted_count += len(delete_ids)
            
            conn.commit()
            
            # Get statistics after cleanup
            cur.execute("SELECT COUNT(*) FROM automated_search_history")
            total_after = cur.fetchone()[0]
            
            print(f"\n✅ Cleanup complete!")
            print(f"   • Before: {total_before} entries")
            print(f"   • After: {total_after} entries")
            print(f"   • Deleted: {deleted_count} duplicates")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    cleanup_duplicates()
