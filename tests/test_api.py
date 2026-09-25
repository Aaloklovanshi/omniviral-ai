import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_auth_me():
    res = client.get("/api/auth/me?email=freeediting35@gmail.com")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["user"]["email"] == "freeediting35@gmail.com"
    print("✓ Auth API verified")

def test_products_list():
    res = client.get("/api/products/list")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert len(data["products"]) >= 4
    print(f"✓ Products API verified ({len(data['products'])} products available)")

def test_video_bundle_generation():
    payload = {
        "user_email": "freeediting35@gmail.com",
        "topic": "How to automate YouTube shorts with AI in 2026",
        "niche": "AI & Tech",
        "target_duration": 30,
        "subtitle_style": "hormozi_bold"
    }
    res = client.post("/api/generate/full-bundle", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "script_data" in data
    assert len(data["script_data"]["hook_variations"]) >= 3
    assert len(data["script_data"]["scenes"]) >= 3
    assert "subtitles" in data
    print("✓ Full Video Bundle Generation API verified")

def test_subtitles_api():
    payload = {
        "text": "Stop wasting hours editing reels when AI does it instantly",
        "duration_seconds": 15.0,
        "preset": "hormozi_bold"
    }
    res = client.post("/api/subtitles/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "srt" in data["data"]
    assert "ass" in data["data"]
    print("✓ Subtitle Styling Engine verified")

def test_billing_plans():
    res = client.get("/api/billing/plans")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "pro" in data["plans"]
    print("✓ Billing Plans API verified")

def test_recon_scan():
    payload = {
        "user_email": "freeediting35@gmail.com",
        "target_domain": "target-test-domain.com",
        "scan_depth": "deep"
    }
    res = client.post("/api/recon/scan", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert len(data["subdomains_found"]) > 0
    assert len(data["findings"]) > 0
    print("✓ Security Recon API verified")

def test_ai_hunt_daily_pack():
    res = client.get("/api/ai-hunt/daily-pack?count=3")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["channel"] == "@ai_hunt"
    assert len(data["packs"]) == 3
    print("✓ @ai_hunt Dedicated Channel Engine verified")

def test_social_publisher():
    # Test Auto Schedule
    res_sched = client.post("/api/social/auto-schedule", json={"channel": "ai_hunt", "count": 2})
    assert res_sched.status_code == 200
    assert res_sched.json()["status"] == "success"
    
    # Test Queue fetch
    res_q = client.get("/api/social/queue")
    assert res_q.status_code == 200
    assert res_q.json()["total_queued"] > 0
    print("✓ Postiz Social Publisher Queue & Dispatch verified")

if __name__ == "__main__":
    test_auth_me()
    test_products_list()
    test_video_bundle_generation()
    test_subtitles_api()
    test_billing_plans()
    test_recon_scan()
    test_ai_hunt_daily_pack()
    test_social_publisher()
    print("\n🎉 ALL API UNIT TESTS PASSED SUCCESSFULLY!")
