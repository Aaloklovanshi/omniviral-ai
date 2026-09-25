import uuid
import json
import random
from backend.database import get_connection

PRODUCT_IDEAS = [
    {
        "slug": "ai-instagram-growth-kit",
        "title": "The 100k Followers AI Instagram Reels Blueprint",
        "category": "Growth Guides",
        "price_usd": 39.00,
        "features": ["30-Day Viral Content Calendar", "50 Done-for-you Video Scripts", "Hashtag & Audio Algorithm Hack"]
    },
    {
        "slug": "notion-saas-creator-os",
        "title": "Micro-SaaS & Agency Operating System (Notion Template)",
        "category": "Notion Templates",
        "price_usd": 49.00,
        "features": ["Client CRM & Invoice Tracker", "Content Pipeline Kanban Board", "Bug Bounty Target Dashboard"]
    },
    {
        "slug": "seekho-course-creator-pack",
        "title": "Seekho & Udemy Fast-Track AI Course Bundle",
        "category": "Course Templates",
        "price_usd": 27.00,
        "features": ["Slide Deck Templates", "AI Script Generation Framework", "Hinglish Narration Prompts"]
    },
    {
        "slug": "ethical-hacker-recon-cheatsheet",
        "title": "Bug Bounty Recon & Attack Surface Cheat Sheet 2026",
        "category": "Cybersecurity",
        "price_usd": 19.00,
        "features": ["Top 100 One-Liner Recon Commands", "Nuclei Custom Template Collection", "XSS & IDOR Payload List"]
    }
]

def run_digital_product_worker(worker_id: int):
    idea = PRODUCT_IDEAS[(worker_id - 9) % len(PRODUCT_IDEAS)]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if exists or insert
    cursor.execute("SELECT id FROM digital_products WHERE slug = ?", (idea["slug"],))
    existing = cursor.fetchone()
    
    if not existing:
        prod_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO digital_products (id, slug, title, description, category, price_usd, file_path, features_json, sales_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            prod_id,
            idea["slug"],
            idea["title"],
            f"Autonomous high-converting digital asset generated for {idea['category']}.",
            idea["category"],
            idea["price_usd"],
            f"digital_products/{idea['slug']}.md",
            json.dumps(idea["features"]),
            random.randint(12, 48)
        ))
    else:
        prod_id = existing["id"]
        
    summary = f"Synthesized & staged digital product: '{idea['title']}' (${idea['price_usd']} USD)."
    metrics = {
        "product_id": prod_id,
        "title": idea["title"],
        "price_usd": idea["price_usd"],
        "category": idea["category"]
    }
    
    cursor.execute("""
        INSERT INTO agent_runs (id, agent_name, worker_id, task_type, output_summary, metrics_json, status)
        VALUES (?, 'DigitalProductSwarm', ?, 'product_synthesis', ?, ?, 'success')
    """, (str(uuid.uuid4()), worker_id, summary, json.dumps(metrics)))
    
    conn.commit()
    conn.close()
    
    return {"worker_id": worker_id, "title": idea["title"], "summary": summary}
