import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import time
import datetime
import os
import json
from agents.orchestrator import run_20_agent_swarm
from backend.services.video_renderer import VideoRenderer
from backend.services.ai_hunt_engine import AIHuntEngine
from backend.services.thumbnail_engine import ThumbnailEngine
OUTPUT_DIR = BASE_DIR / "output" / "daily_batches"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class AutonomousCashflowDaemon:
    """
    24/7 Autonomous Daemon that executes the 20-agent money swarm,
    renders ready-to-post AI video reels for @ai_hunt, and maintains daily content drops.
    """
    def __init__(self, interval_minutes: int = 60):
        self.interval_seconds = interval_minutes * 60
        self.renderer = VideoRenderer()
        self.thumbnail_engine = ThumbnailEngine()
        self.ai_hunt_engine = AIHuntEngine()

    def execute_daily_cycle(self):
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        batch_dir = OUTPUT_DIR / today_str
        batch_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n========================================================")
        print(f"🚀 [AUTONOMOUS DAEMON] STARTING CYCLE: {datetime.datetime.now().isoformat()}")
        print(f"📁 BATCH DIRECTORY: {batch_dir}")
        print(f"========================================================")

        # 1. Run 20-Agent Swarm
        print("\n⚡ [DAEMON STEP 1/3] Executing 20-Agent Revenue Swarm...")
        swarm_result = run_20_agent_swarm()

        # 2. Generate Dedicated @ai_hunt Content Pack
        print("\n🎙️ [DAEMON STEP 2/3] Generating Daily 3-Pack for @ai_hunt...")
        packs = self.ai_hunt_engine.generate_daily_ai_hunt_pack(count=3)
        
        pack_file = batch_dir / "ai_hunt_content_pack.json"
        with open(pack_file, "w", encoding="utf-8") as f:
            json.dump(packs, f, indent=2)
        print(f"✓ Saved @ai_hunt pack to: {pack_file}")

        # 3. Render Sample MP4 Video Reel & High-CTR Thumbnail
        print("\n🎬 [DAEMON STEP 3/3] Rendering Automated MP4 Short Reel & Cover Image...")
        if packs:
            sample = packs[0]
            timestamp = int(time.time())
            vid_filename = f"reel_{timestamp}.mp4"
            thumb_filename = f"thumb_{timestamp}.jpg"
            
            rendered_path = self.renderer.render_short_video(
                topic=sample["title"],
                hook=sample.get("hook", "Stop Scrolling!"),
                filename=f"daily_batches/{today_str}/{vid_filename}",
                duration=6.0
            )
            print(f"✓ Rendered Reel Video: {rendered_path}")

            thumb_path = self.thumbnail_engine.generate_high_ctr_cover(
                title_main=sample["title"][:28],
                highlight_word="VIRAL AI",
                filename=f"{today_str}/{thumb_filename}"
            )
            print(f"✓ Rendered Thumbnail: {thumb_path}")

        print(f"\n🎉 [CYCLE COMPLETE] Next cycle in {self.interval_seconds // 60} minutes.")
        print(f"========================================================\n")

    def run_forever(self):
        print(f"🔥 Autonomous Cashflow Daemon initialized. Running every {self.interval_seconds // 60}m.")
        while True:
            try:
                self.execute_daily_cycle()
            except Exception as e:
                print(f"❌ Error during daemon cycle: {e}")
            time.sleep(self.interval_seconds)

if __name__ == "__main__":
    daemon = AutonomousCashflowDaemon(interval_minutes=60)
    # Run continuous 24/7 autonomous loop
    daemon.run_forever()
