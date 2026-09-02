import sqlite3
from pathlib import Path
from flask import g

DATABASE = Path(__file__).with_name("blog.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)

    # Enable foreign key support
    db.execute("PRAGMA foreign_keys = ON")

    # Create tables
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(user_id, post_id),

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE,

            FOREIGN KEY(post_id)
            REFERENCES posts(id)
            ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE,

            FOREIGN KEY(post_id)
            REFERENCES posts(id)
            ON DELETE CASCADE
        );
    """)

    # Check existing columns in posts table
    columns = [
        row[1]
        for row in db.execute(
            "PRAGMA table_info(posts)"
        ).fetchall()
    ]

    # Add category if it does not already exist
    if "category" not in columns:
        db.execute("""
            ALTER TABLE posts
            ADD COLUMN category TEXT NOT NULL DEFAULT 'General'
        """)

    # Posts indexes
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_posts_user
        ON posts(user_id)
    """)

    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_posts_category
        ON posts(category)
    """)

    # Likes indexes
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_likes_post
        ON likes(post_id)
    """)

    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_likes_user
        ON likes(user_id)
    """)

    # Comments indexes
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_comments_post
        ON comments(post_id)
    """)

    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_comments_user
        ON comments(user_id)
    """)

    db.commit()
    db.close()