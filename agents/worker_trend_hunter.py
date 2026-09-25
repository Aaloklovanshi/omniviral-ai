import time
import random
import uuid
import json
from backend.database import get_connection

TRENDING_NICHES = [
    {
        "niche": "AI Tools & Automation",
        "search_volume_index": 98,
        "cpc_usd": 4.80,
        "trending_queries": [
            "how to use gemini pro for youtube automation",
            "best ai video generator 2026 without watermark",
            "veo 3 vs kling 1.5 comparison prompts",
            "automate instagram reels with python"
        ]
    },
    {
        "niche": "Faceless YouTube Cashflow",
        "search_volume_index": 95,
        "cpc_usd": 3.90,
        "trending_queries": [
            "faceless youtube channel niche ideas 2026",
            "how to get 100k views on shorts in 7 days",
            "viral hook formula alex hormozi subtitles",
            "monetize tiktok in india without vpn"
        ]
    },
    {
        "niche": "Bug Bounty & Cybersecurity",
        "search_volume_index": 89,
        "cpc_usd": 5.40,
        "trending_queries": [
            "bugcrowd recon tools automation tutorial",
            "hexstrike kali linux setup 2026",
            "finding high severity idor vulnerabilities",
            "bounty payout proof for beginners"
        ]
    },
    {
        "niche": "Personal Finance & Micro-SaaS",
        "search_volume_index": 92,
        "cpc_usd": 6.20,
        "trending_queries": [
            "how to build micro saas with python in a weekend",
            "earn 1000 dollars monthly with digital products",
            "gumroad vs lemonsqueezy for selling prompts",
            "passive income ai tools for college students"
        ]
    }
]

def run_trend_worker(worker_id: int):
    """
    Worker function simulating deep search & trend analysis.
    Logs discovery to the SQLite database.
    """
    niche_data = TRENDING_NICHES[(worker_id - 1) % len(TRENDING_NICHES)]
    discovered_topic = random.choice(niche_data["trending_queries"])
    
    summary = f"Identified High-Velocity Trend: '{discovered_topic}' (CPC: ${niche_data['cpc_usd']}, Search Volume Index: {niche_data['search_volume_index']}/100)"
    
    metrics = {
        "niche": niche_data["niche"],
        "top_query": discovered_topic,
        "search_velocity": f"+{random.randint(140, 480)}% this week",
        "monetization_potential": "High ($1.5k - $5k/mo)"
    }
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO agent_runs (id, agent_name, worker_id, task_type, output_summary, metrics_json, status)
        VALUES (?, 'TrendHunterSwarm', ?, 'trend_analysis', ?, ?, 'success')
    """, (str(uuid.uuid4()), worker_id, summary, json.dumps(metrics)))
    conn.commit()
    conn.close()
    
    return {"worker_id": worker_id, "topic": discovered_topic, "summary": summary}
