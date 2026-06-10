import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from nonebot import get_driver

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "summaries.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP NOT NULL,
            content TEXT NOT NULL,
            keywords TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_group_time ON summaries(group_id, end_time)")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS keyword_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            keyword TEXT NOT NULL,
            summary_id INTEGER NOT NULL,
            FOREIGN KEY (summary_id) REFERENCES summaries(id) ON DELETE CASCADE
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_keyword ON keyword_cache(group_id, keyword)")
        conn.execute("""
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        conn.execute("INSERT OR IGNORE INTO meta (key, value) VALUES ('schema_version', '1')")
        conn.commit()

def save_summary(group_id: int, start_time: datetime, end_time: datetime, content: str, keywords: List[str] = None):
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO summaries (group_id, start_time, end_time, content, keywords) VALUES (?, ?, ?, ?, ?)",
            (group_id, start_time, end_time, content, json.dumps(keywords) if keywords else None)
        )
        summary_id = cursor.lastrowid
        if keywords:
            for kw in set(keywords):
                conn.execute(
                    "INSERT INTO keyword_cache (group_id, keyword, summary_id) VALUES (?, ?, ?)",
                    (group_id, kw, summary_id)
                )
        conn.commit()
    return summary_id

def get_recent_summaries(group_id: int, limit: int = 5) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, start_time, end_time, content, keywords, created_at FROM summaries WHERE group_id = ? ORDER BY end_time DESC LIMIT ?",
            (group_id, limit)
        ).fetchall()
    return [dict(row) for row in rows]

def get_summaries_by_time_range(group_id: int, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, start_time, end_time, content, keywords, created_at FROM summaries WHERE group_id = ? AND end_time >= ? AND end_time <= ? ORDER BY end_time ASC",
            (group_id, start_date, end_date)
        ).fetchall()
    return [dict(row) for row in rows]

def get_summaries_by_keyword(group_id: int, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT s.id, s.start_time, s.end_time, s.content, s.keywords, s.created_at FROM summaries s JOIN keyword_cache k ON s.id = k.summary_id WHERE s.group_id = ? AND k.keyword = ? ORDER BY s.end_time DESC LIMIT ?",
            (group_id, keyword, limit)
        ).fetchall()
    return [dict(row) for row in rows]

def get_latest_summary_content(group_id: int) -> Optional[str]:
    rows = get_recent_summaries(group_id, limit=1)
    return rows[0]['content'] if rows else None

init_db()