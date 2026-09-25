import os
import json
import datetime
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests

from backend.config import BASE_DIR
from backend.database import get_connection

POSTIZ_API_URL = os.getenv("POSTIZ_API_URL", "http://localhost:3000/api/v1")
POSTIZ_API_KEY = os.getenv("POSTIZ_API_KEY", "")

class PostizIntegrator:
    """
    Automated Social Publisher integrating with Postiz (100% Open Source & Free)
    Handles automated multi-platform scheduling for YouTube Shorts, Instagram Reels, TikTok, and X.
    """
    def __init__(self, api_url: str = POSTIZ_API_URL, api_key: str = POSTIZ_API_KEY):
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self._init_social_tables()

    def _init_social_tables(self):
        with get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scheduled_social_posts (
                    id TEXT PRIMARY KEY,
                    channel TEXT,
                    platforms TEXT,
                    title TEXT,
                    caption TEXT,
                    hashtags TEXT,
                    media_path TEXT,
                    scheduled_time TEXT,
                    status TEXT DEFAULT 'staged',
                    postiz_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def schedule_daily_batch_to_postiz(self, channel: str = "ai_hunt", video_paths: List[str] = None) -> List[Dict[str, Any]]:
        """
        Schedules a full day's social media content across YouTube Shorts, Instagram, and TikTok.
        Optimizes publish times for peak engagement.
        """
        now = datetime.datetime.now()
        time_slots = [
            now.replace(hour=9, minute=30, second=0, microsecond=0) + datetime.timedelta(days=1),
            now.replace(hour=14, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1),
            now.replace(hour=19, minute=15, second=0, microsecond=0) + datetime.timedelta(days=1),
        ]

        scheduled_items = []
        
        # Pull latest content pack for ai_hunt
        from backend.services.ai_hunt_engine import AIHuntEngine
        engine = AIHuntEngine()
        packs = engine.generate_daily_ai_hunt_pack(count=len(time_slots))

        for idx, pack in enumerate(packs):
            sched_time = time_slots[idx].isoformat()
            post_id = str(uuid.uuid4())
            media_file = video_paths[idx] if video_paths and idx < len(video_paths) else f"output/sample_reel_{idx+1}.mp4"

            payload = {
                "id": post_id,
                "channel": channel,
                "platforms": ["youtube_shorts", "instagram_reels", "tiktok", "twitter_x"],
                "title": pack["youtube_title"],
                "caption": pack["instagram_caption"],
                "hashtags": "#aihunt #aitools #techtrends #viralshorts #geminipro",
                "media_path": media_file,
                "scheduled_time": sched_time,
                "status": "staged"
            }

            # Attempt live Postiz dispatch if API key configured
            if self.api_key:
                try:
                    res = requests.post(
                        f"{self.api_url}/posts",
                        headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                        json={
                            "content": payload["caption"],
                            "scheduledAt": sched_time,
                            "media": [payload["media_path"]],
                            "providers": ["youtube", "instagram", "tiktok"]
                        },
                        timeout=5
                    )
                    if res.status_code in [200, 201]:
                        payload["status"] = "dispatched_to_postiz"
                        payload["postiz_id"] = res.json().get("id", "pz_" + post_id[:8])
                except Exception as e:
                    payload["status"] = f"staged_locally_ready"

            # Save to SQLite
            with get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO scheduled_social_posts 
                    (id, channel, platforms, title, caption, hashtags, media_path, scheduled_time, status, postiz_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    payload["id"],
                    payload["channel"],
                    json.dumps(payload["platforms"]),
                    payload["title"],
                    payload["caption"],
                    payload["hashtags"],
                    payload["media_path"],
                    payload["scheduled_time"],
                    payload["status"],
                    payload.get("postiz_id", "local_staged")
                ))
                conn.commit()

            scheduled_items.append(payload)

        return scheduled_items

    def get_scheduled_posts(self, limit: int = 20) -> List[Dict[str, Any]]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM scheduled_social_posts ORDER BY scheduled_time ASC LIMIT ?", 
                (limit,)
            ).fetchall()
            return [dict(r) for r in rows]
