import os
import sqlite3
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

def seed_admin():
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if not admin_password:
        print("ADMIN_PASSWORD is not set. Add it to your .env file first.")
        return

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin WHERE username = ?", (admin_username,))
    existing = cursor.fetchone()

    if existing:
        print("Admin account already exists. Skipping.")
    else:
        password_hash = generate_password_hash(admin_password)

        cursor.execute('''
            INSERT INTO admin (username, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', (admin_username, password_hash, 'Admin', 'Manager'))

        conn.commit()
        print("Admin account created successfully.")

    conn.close()

if __name__ == '__main__':
    seed_admin()