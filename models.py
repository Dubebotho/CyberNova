import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.executescript('''
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS admin (
            id            INTEGER      PRIMARY KEY AUTOINCREMENT,
            username      VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            first_name    VARCHAR(100) NOT NULL,
            last_name     VARCHAR(100) NOT NULL,
            created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS inquiry (
            id           INTEGER      PRIMARY KEY AUTOINCREMENT,
            admin_id     INT          NULL REFERENCES admin(id),
            name         VARCHAR(150) NOT NULL,
            email        VARCHAR(150) NOT NULL,
            phone        VARCHAR(50)  NULL,
            region       VARCHAR(100) NULL,
            company      VARCHAR(150) NULL,
            service_type VARCHAR(100) NULL,
            message      TEXT         NOT NULL,
            submitted_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
            status       VARCHAR(50)  NOT NULL DEFAULT 'new',
            FOREIGN KEY (admin_id) REFERENCES admin(id)
        );

        CREATE TABLE IF NOT EXISTS testimonial (
            id          INTEGER      PRIMARY KEY AUTOINCREMENT,
            admin_id    INT          NULL,
            client_name VARCHAR(150) NOT NULL,
            company     VARCHAR(150) NULL,
            rating      INT          NOT NULL CHECK(rating BETWEEN 1 AND 5),
            content     TEXT         NOT NULL,
            created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
            approved    BOOLEAN      NOT NULL DEFAULT FALSE,
            FOREIGN KEY (admin_id) REFERENCES admin(id)
        );

        CREATE TABLE IF NOT EXISTS blog_post (
            id           INTEGER      PRIMARY KEY AUTOINCREMENT,
            admin_id     INT          NOT NULL,
            title        VARCHAR(255) NOT NULL,
            content      TEXT         NOT NULL,
            category     VARCHAR(100) NULL,
            cover_image  VARCHAR(255) NULL,
            published_at DATETIME     NULL,
            status       VARCHAR(50)  NOT NULL DEFAULT 'draft',
            FOREIGN KEY (admin_id) REFERENCES admin(id)
        );

        CREATE TABLE IF NOT EXISTS solution (
            id            INTEGER      PRIMARY KEY AUTOINCREMENT,
            admin_id      INT          NOT NULL,
            title         VARCHAR(255) NOT NULL,
            description   TEXT         NOT NULL,
            icon          VARCHAR(255) NULL,
            display_order INT          NOT NULL DEFAULT 0,
            FOREIGN KEY (admin_id) REFERENCES admin(id)
        );

        CREATE TABLE IF NOT EXISTS case_study (
            id         INTEGER      PRIMARY KEY AUTOINCREMENT,
            admin_id   INT          NOT NULL,
            title      VARCHAR(255) NOT NULL,
            client     VARCHAR(150) NOT NULL,
            industry   VARCHAR(100) NULL,
            summary    TEXT         NULL,
            content    TEXT         NOT NULL,
            created_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES admin(id)
        );

        CREATE TABLE IF NOT EXISTS gallery_image (
            id         INTEGER      PRIMARY KEY AUTOINCREMENT,
            admin_id   INT          NULL,
            filename   VARCHAR(255) NOT NULL,
            caption    VARCHAR(255) NULL,
            category   VARCHAR(100) NULL,
            updated_at DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES admin(id)
        );
    ''')

    # ── Migrations: add columns to existing databases ───────
    existing_blog_columns = [
        row[1] for row in cursor.execute('PRAGMA table_info(blog_post)').fetchall()
    ]
    if 'category' not in existing_blog_columns:
        cursor.execute(
            'ALTER TABLE blog_post ADD COLUMN category VARCHAR(100) NULL'
        )
    if 'cover_image' not in existing_blog_columns:
        cursor.execute(
            'ALTER TABLE blog_post ADD COLUMN cover_image VARCHAR(255) NULL'
        )

    existing_inquiry_columns = [
        row[1] for row in cursor.execute('PRAGMA table_info(inquiry)').fetchall()
    ]
    if 'region' not in existing_inquiry_columns:
        cursor.execute(
            'ALTER TABLE inquiry ADD COLUMN region VARCHAR(100) NULL'
        )

    conn.commit()
    conn.close()