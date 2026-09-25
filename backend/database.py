import sqlite3
import json
import uuid
import datetime
from backend.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        name TEXT,
        password_hash TEXT,
        plan TEXT DEFAULT 'free',
        credits INTEGER DEFAULT 100,
        api_key TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Projects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        title TEXT NOT NULL,
        niche TEXT,
        script TEXT,
        scene_breakdown TEXT,
        captions_srt TEXT,
        audio_meta TEXT,
        status TEXT DEFAULT 'completed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    
    # Digital Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS digital_products (
        id TEXT PRIMARY KEY,
        slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        price_usd REAL NOT NULL,
        file_path TEXT,
        features_json TEXT,
        sales_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Transactions / Sales table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        customer_email TEXT,
        product_id TEXT,
        amount REAL NOT NULL,
        currency TEXT DEFAULT 'USD',
        provider TEXT DEFAULT 'stripe',
        status TEXT DEFAULT 'completed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Agent Worker Runs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agent_runs (
        id TEXT PRIMARY KEY,
        agent_name TEXT NOT NULL,
        worker_id INTEGER NOT NULL,
        task_type TEXT NOT NULL,
        output_summary TEXT,
        metrics_json TEXT,
        status TEXT DEFAULT 'success',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Leads / Outreach table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        handle TEXT,
        platform TEXT,
        niche TEXT,
        personalized_pitch TEXT,
        status TEXT DEFAULT 'queued',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Security / Bug Recon Audits table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recon_audits (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        target_domain TEXT NOT NULL,
        scan_type TEXT,
        findings_json TEXT,
        severity_score TEXT,
        report_markdown TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    seed_initial_data(conn)
    conn.close()

def seed_initial_data(conn):
    cursor = conn.cursor()
    
    # Check if default user exists
    cursor.execute("SELECT id FROM users WHERE email = 'freeediting35@gmail.com'")
    user = cursor.fetchone()
    if not user:
        user_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO users (id, email, name, plan, credits, api_key)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            "freeediting35@gmail.com",
            "Alok Lovanshi",
            "agency",
            10000,
            f"ov_{uuid.uuid4().hex[:24]}"
        ))
    else:
        user_id = user["id"]
        
    # Check if digital products seeded
    cursor.execute("SELECT COUNT(*) FROM digital_products")
    if cursor.fetchone()[0] == 0:
        products = [
            (
                str(uuid.uuid4()),
                "faceless-video-playbook",
                "The 2026 AI Video & Faceless Channel Cashflow Playbook",
                "The complete step-by-step master guide to generating $5,000 - $10,000/month with AI-generated faceless channels across YouTube Shorts, Instagram Reels, and TikTok.",
                "E-Books & Playbooks",
                47.00,
                "digital_products/faceless_ai_video_bible.md",
                json.dumps([
                    "8 Comprehensive Chapters from Niche Selection to Monetization",
                    "Complete Viral Prompt Frameworks for Veo 3, Kling, Gemini",
                    "The 3-Second Retention Algorithm & Hook Blueprint",
                    "Affiliate, Sponsorship, and Ad Revenue funnels"
                ]),
                142
            ),
            (
                str(uuid.uuid4()),
                "viral-hook-vault-500",
                "500+ Retention-Engineered Viral Hook Vault",
                "A battle-tested swipe file of 500 psychological video hooks that stop the scroll in under 1.5 seconds, proven to increase watch-through rate by 340%.",
                "Swipe Files & Templates",
                29.00,
                "digital_products/viral_hook_vault_500.json",
                json.dumps([
                    "10 High-CPC Niches (Finance, Tech, Self-Improvement, Storytelling)",
                    "Controversy & Curiosity Gap Formulae",
                    "Hormozi & MrBeast Pacing Formulas",
                    "Ready to copy-paste into OmniViral Studio"
                ]),
                289
            ),
            (
                str(uuid.uuid4()),
                "gemini-veo-master-prompts",
                "250+ Master Prompts for Seekho, Kling & Veo 3",
                "The ultimate production-ready AI video prompt library. Generates cinematic 4k B-roll, photorealistic characters, and engaging anime animations in one click.",
                "Prompt Libraries",
                37.00,
                "digital_products/gemini_veo_prompt_pack.json",
                json.dumps([
                    "Cinematic Camera Angles & Lighting Tokens",
                    "Consistent Character Seed Generators",
                    "Negative Prompt Blockers for Artefact-Free Generation",
                    "Tested on Gemini 2.0, Veo 3, Kling 1.5, Midjourney v6"
                ]),
                215
            ),
            (
                str(uuid.uuid4()),
                "bug-bounty-recon-suite",
                "Modern VAPT & Bug Bounty Recon Intelligence Pack",
                "Professional attack surface discovery and bug bounty automation suite for security researchers to find high-payout vulnerabilities faster.",
                "Security & Developer Tools",
                67.00,
                "digital_products/bug_bounty_recon_playbook.md",
                json.dumps([
                    "Subdomain Takeover & Exposed Secrets Checklist",
                    "Automated Markdown Report Templates for HackerOne & Bugcrowd",
                    "HexStrike & Kali Linux Tooling Integration Guide",
                    "Real Vulnerability PoC Patterns (IDOR, SSRF, CORS)"
                ]),
                98
            )
        ]
        
        cursor.executemany("""
            INSERT INTO digital_products (id, slug, title, description, category, price_usd, file_path, features_json, sales_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, products)
        
    conn.commit()

# Run init on import
init_db()
