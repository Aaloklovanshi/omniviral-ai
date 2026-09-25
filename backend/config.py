import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "omniviral.db"
STATIC_DIR = BASE_DIR / "frontend"
DIGITAL_PRODUCTS_DIR = BASE_DIR / "digital_products"

# Secret and API configuration
SECRET_KEY = os.getenv("SECRET_KEY", "omniviral-super-secret-production-key-2026")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
LEMONSQUEEZY_API_KEY = os.getenv("LEMONSQUEEZY_API_KEY", "")

# Monetization & Credit Defaults
DEFAULT_SIGNUP_CREDITS = 100
CREDIT_COST_PER_SCRIPT = 5
CREDIT_COST_PER_STORYBOARD = 10
CREDIT_COST_PER_CAPTIONS = 5
CREDIT_COST_PER_VOICEOVER = 15
CREDIT_COST_PER_FULL_BUNDLE = 25

PRICING_PLANS = {
    "starter": {
        "name": "Starter Creator",
        "price_monthly": 19,
        "price_yearly": 190,
        "credits": 500,
        "features": [
            "50 AI Video Scripts / month",
            "Auto Hormozi Animated Captions",
            "Veo 3 & Kling 1.5 Video Prompts",
            "720p/1080p Export Presets",
            "Standard Multi-lingual Voiceovers"
        ]
    },
    "pro": {
        "name": "Pro Viral Engine",
        "price_monthly": 49,
        "price_yearly": 490,
        "credits": 2000,
        "popular": True,
        "features": [
            "Unlimited AI Video Scripts",
            "Complete Faceless Video Storyboards",
            "Viral Hook Controversy Scorer",
            "B-Roll & Ambient Audio Matching",
            "Direct Social Media Multi-Exporter",
            "Priority Support & Gemini 2.0 Pro Engine"
        ]
    },
    "agency": {
        "name": "Agency & Automation Swarm",
        "price_monthly": 99,
        "price_yearly": 990,
        "credits": 6000,
        "features": [
            "Everything in Pro Tier",
            "Autonomous 20-Agent Lead & Content Swarm",
            "Custom Branded Dynamic Watermarks",
            "Full API Access & Webhook Integrations",
            "White-label Client Delivery Portal",
            "Bug Bounty Recon & DevSecOps Audit Module"
        ]
    }
}
