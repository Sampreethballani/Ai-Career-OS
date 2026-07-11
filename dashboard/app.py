import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request
from src.utils.db import init_db, Opportunity
from src.config_manager import config_manager

def run_career_tracker():
    print("⏰ Background Agent Triggered: Running main tracking script...")
    try:
        subprocess.Popen(["python", "src/main.py"])
    except Exception as e:
        print(f"❌ Error running tracker: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=run_career_tracker, trigger="interval", hours=6)
scheduler.start()

app = Flask(__name__)
Session = init_db(config_manager.get("DATABASE_URL"))

@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    per_page = 20
    category = request.args.get("category", "")
    source = request.args.get("source", "")
    min_score = request.args.get("min_score", 0, type=int)
    search = request.args.get("search", "").strip()
    sort = request.args.get("sort", "created_at")
    order = request.args.get("order", "desc")

    session = Session()
    query = session.query(Opportunity)

    if category:
        query = query.filter(Opportunity.category == category)
    if source:
        query = query.filter(Opportunity.source == source)
    if min_score:
        query = query.filter(Opportunity.relevance_score >= min_score)
    if search:
        query = query.filter(
            Opportunity.title.ilike(f"%{search}%") |
            Opportunity.company.ilike(f"%{search}%") |
            Opportunity.description.ilike(f"%{search}%")
        )

    sort_col = getattr(Opportunity, sort, Opportunity.created_at)
    if order == "asc":
        query = query.order_by(sort_col.asc())
    else:
        query = query.order_by(sort_col.desc())

    total = query.count()
    opportunities = query.offset((page - 1) * per_page).limit(per_page).all()

    categories = [r[0] for r in session.query(Opportunity.category).distinct().all()]
    sources = [r[0] for r in session.query(Opportunity.source).distinct().all()]

    session.close()

    return render_template(
        "index.html",
        opportunities=opportunities,
        page=page,
        total=total,
        per_page=per_page,
        category=category,
        source=source,
        min_score=min_score,
        search=search,
        sort=sort,
        order=order,
        categories=categories,
        sources=sources,
    )

@app.route("/stats")
def stats():
    session = Session()
    total = session.query(Opportunity).count()
    by_category = (
        session.query(Opportunity.category, Opportunity.relevance_score)
        .all()
    )
    cat_counts = {}
    for cat, score in by_category:
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

    notified = session.query(Opportunity).filter(Opportunity.is_notified == True).count()
    avg_score = session.query(Opportunity.relevance_score).filter(Opportunity.relevance_score > 0).all()
    avg = sum(s[0] for s in avg_score) / len(avg_score) if avg_score else 0

    by_source = (
        session.query(Opportunity.source)
        .all()
    )
    src_counts = {}
    for s in by_source:
        src_counts[s[0]] = src_counts.get(s[0], 0) + 1

    session.close()
    return render_template(
        "stats.html",
        total=total,
        cat_counts=cat_counts,
        notified=notified,
        avg_score=round(avg, 1),
        src_counts=src_counts,
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
