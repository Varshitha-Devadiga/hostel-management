import sqlite3

def migrate():
    conn = sqlite3.connect('e:/bcwd/instance/bcwd.db')
    cursor = conn.cursor()
    try:
        cursor.execute('ALTER TABLE leave_requests ADD COLUMN is_returned BOOLEAN DEFAULT 0')
        cursor.execute('ALTER TABLE leave_requests ADD COLUMN return_time VARCHAR(10)')
        cursor.execute('ALTER TABLE leave_requests ADD COLUMN return_notes TEXT')
        print("Successfully added new columns.")
    except Exception as e:
        print("Error or already exists:", e)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    migrate()
