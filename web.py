import os
import sys
from pathlib import Path
from flask import Flask, render_template, request
from config import Config
from my_fetcher import fetch_raw_news
from my_filter import evaluate_article


def _resource_path(relative_path):
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return str(base_dir / relative_path)


def create_app():
    template_folder = _resource_path("templates")
    static_folder = _resource_path("static")
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

    @app.route("/")
    def index():
        query = request.args.get("q", "technology").strip()
        if not query:
            query = "technology"

        error = None
        results = []
        show_authenticity = bool(Config.GROQ_API_KEY)

        if not Config.NEWS_API_KEY:
            error = "Missing NEWS_API_KEY. Add it to .env and restart the app."
        else:
            articles = fetch_raw_news(query=query)
            if not articles:
                error = "No articles were found. Please check your query or your News API key."
            else:
                for article in articles[:8]: # Limits to top 8 stories
                    title = article.get("title") or "Untitled"
                    description = article.get("description") or article.get("content") or "No description available."
                    source = article.get("source", {}).get("name") or "Unknown source"
                    url = article.get("url")
                    published = article.get("publishedAt")

                    authenticity, reason = None, None
                    if show_authenticity and title:
                        evaluation = evaluate_article(title, description)
                        authenticity = evaluation.get("is_authentic")
                        reason = evaluation.get("reason")
                    elif not show_authenticity:
                        reason = "Missing GROQ_API_KEY; authenticity checks are disabled."

                    results.append({
                        "title": title, "description": description, "source": source,
                        "url": url, "published": published, "authenticity": authenticity,
                        "reason": reason,
                    })

        return render_template("index.html", query=query, results=results, error=error, show_authenticity=show_authenticity)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
