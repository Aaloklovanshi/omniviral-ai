from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid
import json
from backend.database import get_connection
from backend.services.gemini_service import AIScriptEngine
from backend.services.subtitle_styler import SubtitleEngine
from backend.services.audio_service import AudioEngine
from backend.config import CREDIT_COST_PER_FULL_BUNDLE

router = APIRouter(prefix="/api/generate", tags=["ai_generator"])
script_engine = AIScriptEngine()
subtitle_engine = SubtitleEngine()
audio_engine = AudioEngine()

class VideoGenRequest(BaseModel):
    user_email: str = "freeediting35@gmail.com"
    topic: str
    niche: Optional[str] = "AI & Tech"
    tone: Optional[str] = "energetic"
    target_duration: Optional[int] = 45
    subtitle_style: Optional[str] = "hormozi_bold"
    voice_id: Optional[str] = "marcus_deep"

class HookAnalyzeRequest(BaseModel):
    script_text: str

@router.post("/full-bundle")
def generate_full_video_bundle(payload: VideoGenRequest):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check user credits
    cursor.execute("SELECT * FROM users WHERE email = ?", (payload.user_email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        
    if user["credits"] < CREDIT_COST_PER_FULL_BUNDLE:
        conn.close()
        raise HTTPException(status_code=400, detail="Insufficient credits. Please upgrade your plan.")
        
    # Deduct credits
    new_credits = user["credits"] - CREDIT_COST_PER_FULL_BUNDLE
    cursor.execute("UPDATE users SET credits = ? WHERE id = ?", (new_credits, user["id"]))
    
    # Generate content using AI Engines
    script_data = script_engine.generate_viral_script(
        topic=payload.topic,
        niche=payload.niche,
        tone=payload.tone,
        target_duration=payload.target_duration
    )
    
    # Generate Subtitles
    subs = subtitle_engine.generate_timed_subtitles(
        script_text=script_data["full_voiceover_script"],
        total_duration=float(payload.target_duration),
        preset=payload.subtitle_style
    )
    
    # Audio Plan
    audio_data = audio_engine.plan_audio_track(
        script_text=script_data["full_voiceover_script"],
        voice_id=payload.voice_id
    )
    
    # Save project to database
    project_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO projects (id, user_id, title, niche, script, scene_breakdown, captions_srt, audio_meta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        project_id,
        user["id"],
        script_data["title"],
        payload.niche,
        script_data["full_voiceover_script"],
        json.dumps(script_data["scenes"]),
        subs["srt"],
        json.dumps(audio_data)
    ))
    
    conn.commit()
    conn.close()
    
    return {
        "status": "success",
        "project_id": project_id,
        "remaining_credits": new_credits,
        "script_data": script_data,
        "subtitles": subs,
        "audio_data": audio_data
    }

@router.post("/analyze-hooks")
def analyze_hooks(payload: HookAnalyzeRequest):
    result = script_engine.analyze_controversy_and_hooks(payload.script_text)
    return {"status": "success", "analysis": result}

@router.get("/projects")
def list_user_projects(email: str = "freeediting35@gmail.com"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.* FROM projects p
        JOIN users u ON p.user_id = u.id
        WHERE u.email = ?
        ORDER BY p.created_at DESC
    """, (email,))
    rows = cursor.fetchall()
    conn.close()
    
    projects = []
    for r in rows:
        p_dict = dict(r)
        if p_dict.get("scene_breakdown"):
            p_dict["scene_breakdown"] = json.loads(p_dict["scene_breakdown"])
        if p_dict.get("audio_meta"):
            p_dict["audio_meta"] = json.loads(p_dict["audio_meta"])
        projects.append(p_dict)
        
    return {"status": "success", "projects": projects}
