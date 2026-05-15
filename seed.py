import sqlite3
from werkzeug.security import generate_password_hash

def seed_admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
    existing = cursor.fetchone()

    if existing:
        print("Admin account already exists. Skipping.")
    else:
        password_hash = generate_password_hash('admin123')

        cursor.execute('''
            INSERT INTO admin (username, password_hash, first_name, last_name)
            VALUES (?, ?, ?, ?)
        ''', ('admin', password_hash, 'Thabang', 'Dube'))

        conn.commit()
        print("Admin account created successfully.")

    conn.close()

if __name__ == '__main__':
    seed_admin()