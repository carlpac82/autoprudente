"""
Fix WhatsApp conversations with contact_id = 0

This script finds all conversations with contact_id = 0 and sets them to NULL
so the foreign key constraint doesn't fail.
"""

import os
import psycopg2

def fix_contact_id_zero():
    """Fix conversations with contact_id = 0 by setting to NULL"""
    
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL not found in environment")
        return
    
    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        # Find conversations with contact_id = 0
        cur.execute("""
            SELECT id, phone_number, contact_id 
            FROM whatsapp_conversations 
            WHERE contact_id = 0
        """)
        
        bad_rows = cur.fetchall()
        
        if not bad_rows:
            print("✅ No conversations with contact_id = 0 found")
            conn.close()
            return
        
        print(f"⚠️  Found {len(bad_rows)} conversations with contact_id = 0:")
        for row in bad_rows:
            print(f"   - Conversation #{row[0]}: phone={row[1]}, contact_id={row[2]}")
        
        # Fix them by setting to NULL
        cur.execute("""
            UPDATE whatsapp_conversations 
            SET contact_id = NULL 
            WHERE contact_id = 0
        """)
        
        affected = cur.rowcount
        conn.commit()
        
        print(f"✅ Fixed {affected} conversations (set contact_id to NULL)")
        
        # Also check for any other invalid contact_id values
        cur.execute("""
            SELECT DISTINCT wc.contact_id
            FROM whatsapp_conversations wc
            LEFT JOIN whatsapp_contacts c ON wc.contact_id = c.id
            WHERE wc.contact_id IS NOT NULL 
            AND c.id IS NULL
        """)
        
        orphaned = cur.fetchall()
        if orphaned:
            print(f"⚠️  Found {len(orphaned)} conversations with orphaned contact_id values:")
            for row in orphaned:
                print(f"   - contact_id={row[0]} (contact doesn't exist)")
            
            # Fix them too
            cur.execute("""
                UPDATE whatsapp_conversations 
                SET contact_id = NULL 
                WHERE contact_id IS NOT NULL 
                AND contact_id NOT IN (SELECT id FROM whatsapp_contacts)
            """)
            
            affected = cur.rowcount
            conn.commit()
            print(f"✅ Fixed {affected} orphaned contact_id values")
        
        conn.close()
        print("\n✅ Database cleanup completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_contact_id_zero()
