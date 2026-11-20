from flask import Blueprint, jsonify, render_template, request

from app import db
from app.database import search_knowledge_base
from app.services.internet_search import search_internet


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/api/search")
def search():
    query = request.args.get("q", "").strip()

    if not query:
        return jsonify({
            "query": "",
            "count": 0,
            "knowledge_base": [],
            "internet": {
                "images": [],
                "videos": [],
                "news": [],
                "youtube_configured": False
            }
        })

    try:
        # Поиск в собственной базе PostgreSQL
        knowledge_results = search_knowledge_base(query)

        # Поиск материалов в интернете
        internet_results = search_internet(query)

        return jsonify({
            "query": query,
            "count": len(knowledge_results),
            "knowledge_base": knowledge_results,
            "internet": internet_results
        })

    except Exception:
        db.session.rollback()

        return jsonify({
            "error": "Не удалось выполнить поиск. Попробуйте ещё раз."
        }), 500
