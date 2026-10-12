
import sqlite3
import uuid
from pathlib import Path

DB_PATH = Path(__file__).parent / "chat_history.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL DEFAULT 'New conversation',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id) ON DELETE CASCADE
            );
        """)


def create_conversation():
    conversation_id = str(uuid.uuid4())

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO conversations (id) VALUES (?)",
            (conversation_id,)
        )

    return conversation_id


def list_conversations():
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, title, created_at, updated_at
            FROM conversations
            ORDER BY updated_at DESC, created_at DESC
        """).fetchall()


def save_message(conversation_id, role, content):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO messages (conversation_id, role, content)
            VALUES (?, ?, ?)
        """, (conversation_id, role, content))

        conn.execute("""
            UPDATE conversations
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (conversation_id,))


def get_messages(conversation_id):
    with get_connection() as conn:
        return conn.execute("""
            SELECT role, content, created_at
            FROM messages
            WHERE conversation_id = ?
            ORDER BY id ASC
        """, (conversation_id,)).fetchall()


def update_title(conversation_id, title):
    title = title.strip().replace("\n", " ")[:50] or "New conversation"

    with get_connection() as conn:
        conn.execute("""
            UPDATE conversations
            SET title = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (title, conversation_id))


def clear_messages(conversation_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM messages WHERE conversation_id = ?",
            (conversation_id,)
        )

        conn.execute("""
            UPDATE conversations
            SET title = 'New conversation',
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (conversation_id,))
