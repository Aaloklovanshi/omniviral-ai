from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.services.subtitle_styler import SubtitleEngine

router = APIRouter(prefix="/api/subtitles", tags=["subtitles"])
engine = SubtitleEngine()

class SubtitleRequest(BaseModel):
    text: str
    duration_seconds: Optional[float] = 30.0
    preset: Optional[str] = "hormozi_bold"

@router.post("/generate")
def generate_subtitles(payload: SubtitleRequest):
    result = engine.generate_timed_subtitles(
        script_text=payload.text,
        total_duration=payload.duration_seconds,
        preset=payload.preset
    )
    return {"status": "success", "data": result}

@router.get("/presets")
def get_presets():
    return {"status": "success", "presets": engine.STYLE_PRESETS}
