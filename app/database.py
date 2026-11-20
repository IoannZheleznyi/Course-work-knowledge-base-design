from pathlib import Path

from sqlalchemy import text

from app import db


SEARCH_SQL_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "queries"
    / "search.sql"
)


def search_knowledge_base(query):
    """Возвращает найденные специи из PostgreSQL."""

    sql = SEARCH_SQL_PATH.read_text(encoding="utf-8")

    rows = db.session.execute(
        text(sql),
        {"query": query}
    ).scalars().all()

    return rows
