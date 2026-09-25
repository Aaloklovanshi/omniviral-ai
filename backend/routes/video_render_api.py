import os
import uuid
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.services.video_renderer import VideoRenderer, OUTPUT_DIR

router = APIRouter(prefix="/api/video", tags=["video_renderer"])
renderer = VideoRenderer()

class RenderVideoRequest(BaseModel):
    topic: str = "Top 3 Secret AI Tools in 2026"
    hook: str = "Stop Scrolling!"
    duration: float = 6.0

@router.post("/render")
def render_video_endpoint(payload: RenderVideoRequest):
    try:
        vid_id = f"ai_hunt_{uuid.uuid4().hex[:8]}.mp4"
        file_path = renderer.render_short_video(
            topic=payload.topic,
            hook=payload.hook,
            filename=vid_id,
            duration=payload.duration
        )
        return {
            "status": "success",
            "message": "Video rendered successfully!",
            "video_id": vid_id,
            "download_url": f"/api/video/download/{vid_id}",
            "stream_url": f"/api/video/stream/{vid_id}",
            "file_path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rendering error: {str(e)}")

@router.get("/download/{filename}")
def download_rendered_video(filename: str):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="video/mp4"
    )

@router.get("/stream/{filename}")
def stream_rendered_video(filename: str):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")
    return FileResponse(
        path=str(file_path),
        media_type="video/mp4"
    )
