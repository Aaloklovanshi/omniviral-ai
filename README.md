# ⚡ OmniViral AI — Autonomous Money System & Production SaaS

> **A Complete Production-Grade AI Video Studio, Digital Asset Store & 20-Agent Autonomous Cashflow Swarm.**  
> *Target Goal: Generate $1,000+ / month within 90–120 days through automated subscriptions, digital asset sales, and multi-platform distribution.*

---

## 🌟 1. System Overview & Architecture

OmniViral AI is engineered as an end-to-end autonomous revenue platform designed for minimal manual interaction. It combines **high-converting software capabilities (SaaS)** with **automated lead discovery**, **viral content generation**, and **pre-built sellable digital assets**.

```
                           ┌────────────────────────────────────────────────────────┐
                           │               OMNIVIRAL AI ARCHITECTURE                │
                           └──────────────────────────┬─────────────────────────────┘
                                                      │
         ┌────────────────────────────────────────────┼────────────────────────────────────────────┐
         │                                            │                                            │
         ▼                                            ▼                                            ▼
┌──────────────────┐                       ┌─────────────────────┐                      ┌──────────────────────┐
│  Web SaaS Studio │                       │  20-Agent Swarm     │                      │  Digital Asset Store │
│  (Next-Gen UI)   │                       │  (Autonomous Engine)│                      │  (Instant Cashflow)  │
├──────────────────┤                       ├─────────────────────┤                      ├──────────────────────┤
│ • Gemini Scripts │                       │ • Trend Hunter (4)  │                      │ • Faceless Playbook  │
│ • Storyboards    │                       │ • Content Factory(4)│                      │ • 500+ Hook Vault    │
│ • Hormozi Subs   │                       │ • Digital Prod (4)  │                      │ • Veo 3 Prompts      │
│ • Security Recon │                       │ • Lead Outreach (4) │                      │ • Bug Bounty Pack    │
│ • Stripe Billing │                       │ • Revenue Opt (4)   │                      │ • Instant Download   │
└──────────────────┘                       └─────────────────────┘                      └──────────────────────┘
```

---

## 💰 2. The 3 Revenue Streams ($1,000/mo Blueprint)

| Stream | Product / Offering | Price Point | Monthly Target for $1,000/mo |
|---|---|---|---|
| **Stream 1: SaaS Subscriptions** | Pro Viral Engine ($49/mo) / Agency Swarm ($99/mo) | $49 - $99 / mo | **15 - 20 Paying Users** |
| **Stream 2: Digital Products** | Faceless Video Playbook, Hook Vault, Veo Prompts | $29 - $67 / sale | **20 - 30 Sales / month** |
| **Stream 3: Bug Bounty & Recon** | Security Audit Reports & Attack Surface Recon | $300 - $1,500 / bounty | **1 - 2 Bounties / month** |

---

## 🤖 3. The 20 Autonomous Agent Workers Breakdown

The system runs 20 specialized concurrent worker threads in `agents/`:

1. **Workers 01 - 04 (Trend Hunter Swarm):**
   - Discovers breakout search terms, high-CPC topics, and algorithm velocity across YouTube, TikTok, and Google.
2. **Workers 05 - 08 (Content & Video Production Swarm):**
   - Automatically generates multi-hook scripts, scene-by-scene prompts for Google Veo 3 / Kling, and Alex Hormozi animated subtitle files.
3. **Workers 09 - 12 (Digital Product Builder Swarm):**
   - Synthesizes and stages ready-to-sell eBooks, prompt libraries, and Notion templates for Gumroad/Payhip.
4. **Workers 13 - 16 (B2B Lead Generation & Outreach Swarm):**
   - Finds high-intent creators, agency founders, and e-commerce stores; generates personalized cold pitch emails and DMs.
5. **Workers 17 - 20 (Revenue & Monetization Optimization Swarm):**
   - Analyzes price elasticity, tracks affiliate commissions, and logs performance metrics directly to SQLite.

---

## 🚀 4. Quick Start & Execution Guide

### Step 1: Launch Everything with 1 Click
Double-click `start_all.bat` or run:
```bash
# In Git Bash / Terminal:
cd C:/Users/aalok/omniviral-ai
python start_server.py
```
Open your browser at **`http://localhost:8000`**.

### Step 2: Run the 20 Autonomous Agents on Demand
```bash
python agents/orchestrator.py
```

### Step 3: Run Automated Verification Tests
```bash
python tests/test_api.py
python tests/test_agents.py
python tests/test_db.py
```

---

## 📁 5. Directory Structure

```
C:\Users\aalok\omniviral-ai\
├── README.md                      # Complete System Documentation
├── start_all.bat                  # 1-Click Launch (SaaS + Swarm)
├── start_agents.bat               # 1-Click Launch (20-Agent Swarm)
├── start_server.py                # Fast ASGI Server Runner
├── .env.example                   # API Keys Template
│
├── backend/                       # REST API & Database
│   ├── app.py                     # FastAPI Application
│   ├── database.py                # SQLite Persistence & Seeding
│   ├── config.py                  # System Constants & Plans
│   ├── routes/                    # Auth, Video Gen, Subtitles, Products, Billing, Recon
│   └── services/                  # Gemini Script Engine, Hormozi Subtitles, Audio Planner
│
├── frontend/                      # Modern Dark Glassmorphism Web App
│   ├── index.html                 # Hero Page & Interactive Studio
│   ├── ai_hunt.html               # Dedicated @ai_hunt Viral Studio
│   ├── social_publisher.html      # Postiz Social Dispatch & Scheduler
│   ├── digital_products.html      # Digital Storefront
│   ├── recon_studio.html          # Bug Bounty & Security Recon Suite
│   ├── styles.css                 # Custom Glassmorphic Dark Design
│   └── app.js                     # Interactive Client Controller
│
├── agents/                        # 20 Autonomous Revenue Workers
│   ├── continuous_daemon.py       # 24/7 Autonomous Scheduler Daemon
│   ├── orchestrator.py            # Master ThreadPool Swarm Coordinator
│   ├── worker_trend_hunter.py     # Workers 1-4 (Trend Discovery)
│   ├── worker_content_factory.py  # Workers 5-8 (Video Packs)
│   ├── worker_digital_product.py  # Workers 9-12 (Asset Builder)
│   ├── worker_lead_outreach.py    # Workers 13-16 (Cold Outreach)
│   └── worker_revenue_optimizer.py# Workers 17-20 (Monetization)
│
├── digital_products/              # Pre-Built $1,000 Asset Inventory
│   ├── faceless_ai_video_bible.md # 8-Chapter Faceless Channel Guide
│   ├── viral_hook_vault_500.json  # 500+ Categorized Viral Hooks
│   ├── gemini_veo_prompt_pack.json# 250+ Cinematic Video Prompts
│   └── bug_bounty_recon_playbook.md# Modern Attack Surface & VAPT Guide
│
└── tests/                         # Full Unit & Integration Test Suite
    ├── test_api.py                # Validates all REST Endpoints
    ├── test_agents.py             # Validates 20/20 Swarm Execution
    └── test_db.py                 # Validates Data Transactions
```

---

## 📈 6. 90-Day Execution Roadmap to $1,000+/Month

```
Month 1: Foundation & Asset Staging
├── Run Swarm daily to generate 10 video bundles per day
├── List the 4 pre-built digital products on Gumroad & Payhip
└── Post 2 AI Shorts/Reels daily on YouTube & Instagram

Month 2: Initial Sales & Outbound Outreach
├── Reach 10–15 digital product sales ($300 - $600)
├── Send 20 personalized B2B outreach pitches generated by Agent Swarm
└── Acquire first 3–5 SaaS beta subscribers ($150 - $250 MRR)

Month 3-4: Scale & Full Automation
├── Scale SaaS to 20+ active subscribers ($1,000+ MRR)
├── Autonomous Lead Swarm generates 50 warm creator leads weekly
└── Target high-payout Bug Bounty disclosures ($500+ rewards)
```

---
*Built with ❤️ by Alok Lovanshi & OmniViral AI Engine.*
