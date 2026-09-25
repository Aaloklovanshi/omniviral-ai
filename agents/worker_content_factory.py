import uuid
import json
import random
from backend.database import get_connection
from backend.services.gemini_service import AIScriptEngine
from backend.services.subtitle_styler import SubtitleEngine
from backend.services.audio_service import AudioEngine

script_engine = AIScriptEngine()
subtitle_engine = SubtitleEngine()
audio_engine = AudioEngine()

SEED_TOPICS = [
    ("How to build a 6-figure AI video brand in 90 days", "AI & Automation"),
    ("The secret bug bounty method that paid $10,000", "Cybersecurity"),
    ("Why 99% of creators fail at YouTube Shorts", "Content Creation"),
    ("The 3 AI tools that will make you $100/day in 2026", "Make Money Online")
]

def run_content_worker(worker_id: int):
    topic, niche = SEED_TOPICS[(worker_id - 5) % len(SEED_TOPICS)]
    
    script_data = script_engine.generate_viral_script(topic=topic, niche=niche, target_duration=35)
    subs = subtitle_engine.generate_timed_subtitles(script_data["full_voiceover_script"], 35.0)
    audio = audio_engine.plan_audio_track(script_data["full_voiceover_script"])
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check default user
    cursor.execute("SELECT id FROM users LIMIT 1")
    user = cursor.fetchone()
    user_id = user["id"] if user else str(uuid.uuid4())
    
    # Save project
    proj_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO projects (id, user_id, title, niche, script, scene_breakdown, captions_srt, audio_meta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        proj_id,
        user_id,
        f"[Autonomous] {script_data['title']}",
        niche,
        script_data["full_voiceover_script"],
        json.dumps(script_data["scenes"]),
        subs["srt"],
        json.dumps(audio)
    ))
    
    summary = f"Generated complete viral video asset pack for '{topic}' with {len(script_data['scenes'])} scenes and Alex Hormozi captions."
    metrics = {
        "project_id": proj_id,
        "scenes_count": len(script_data["scenes"]),
        "words_count": len(script_data["full_voiceover_script"].split()),
        "viral_index": script_data["viral_score"]
    }
    
    cursor.execute("""
        INSERT INTO agent_runs (id, agent_name, worker_id, task_type, output_summary, metrics_json, status)
        VALUES (?, 'ContentFactorySwarm', ?, 'video_bundle_generation', ?, ?, 'success')
    """, (str(uuid.uuid4()), worker_id, summary, json.dumps(metrics)))
    
    conn.commit()
    conn.close()
    
    return {"worker_id": worker_id, "project_id": proj_id, "summary": summary}
