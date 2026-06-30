import sqlite3

def migrate():
    conn = sqlite3.connect('e:/bcwd/instance/bcwd.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE notifications ADD COLUMN target_user_id INTEGER")
        cursor.execute("ALTER TABLE notifications ADD COLUMN target_role VARCHAR(20)")
    except Exception as e:
        print("Error:", e)
    
    # We should update "Document Verification Failed" to target the specific user if possible.
    # But since we don't have user_id easily accessible for existing ones, let's just make them target_role='warden'
    # so they don't spam students.
    cursor.execute("UPDATE notifications SET target_role='warden' WHERE title LIKE '%Verification Failed%'")
    
    conn.commit()
    conn.close()
    print("Migration successful")

if __name__ == "__main__":
    migrate()
