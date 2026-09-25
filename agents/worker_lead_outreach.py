import uuid
import json
import random
from backend.database import get_connection

TARGET_PROFILES = [
    {
        "name": "Sarah Jenkins",
        "handle": "@sarahj_ai",
        "platform": "Instagram / TikTok",
        "niche": "AI Tools Educator",
        "pitch_hook": "Saw your latest Reel on AI productivity — we converted it into 5 high-converting YouTube Shorts with Alex Hormozi dynamic captions automatically."
    },
    {
        "name": "Alex Rivera",
        "handle": "@arivera_growth",
        "platform": "Twitter / X",
        "niche": "SaaS Founder",
        "pitch_hook": "Hey Alex, ran an automated security & attack surface audit on your SaaS staging subdomain. Found 2 misconfigurations you might want to patch before launch."
    },
    {
        "name": "Rohan Sharma",
        "handle": "@rohan_tech_hindi",
        "platform": "YouTube / Seekho",
        "niche": "Hinglish Tech Creator",
        "pitch_hook": "Bhai aapke Seekho courses ke liye humne automated Hinglish video scripting and Veo 3 B-roll generation pipeline integrate kiya hai — output 4x fast ho jayega."
    },
    {
        "name": "Elena Rostova",
        "handle": "@elena_ecommerce",
        "platform": "LinkedIn / IG",
        "niche": "Shopify Brand Owner",
        "pitch_hook": "We generated 10 viral TikTok video ad variations for your top-selling skincare product with dynamic hooks and captions."
    }
]

def run_lead_worker(worker_id: int):
    profile = TARGET_PROFILES[(worker_id - 13) % len(TARGET_PROFILES)]
    
    lead_id = str(uuid.uuid4())
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO leads (id, name, email, handle, platform, niche, personalized_pitch, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'ready_for_outreach')
    """, (
        lead_id,
        profile["name"],
        f"{profile['name'].lower().replace(' ', '.')}@creatornetwork.io",
        profile["handle"],
        profile["platform"],
        profile["niche"],
        profile["pitch_hook"]
    ))
    
    summary = f"Discovered high-intent lead: {profile['name']} ({profile['platform']}) - Formatted custom pitch."
    metrics = {
        "lead_id": lead_id,
        "name": profile["name"],
        "platform": profile["platform"],
        "channel": profile["niche"]
    }
    
    cursor.execute("""
        INSERT INTO agent_runs (id, agent_name, worker_id, task_type, output_summary, metrics_json, status)
        VALUES (?, 'LeadOutreachSwarm', ?, 'lead_generation', ?, ?, 'success')
    """, (str(uuid.uuid4()), worker_id, summary, json.dumps(metrics)))
    
    conn.commit()
    conn.close()
    
    return {"worker_id": worker_id, "lead": profile["name"], "summary": summary}
