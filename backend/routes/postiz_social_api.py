from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from backend.services.postiz_integrator import PostizIntegrator

router = APIRouter(prefix="/api/social", tags=["social_publisher"])
integrator = PostizIntegrator()

class ScheduleRequest(BaseModel):
    channel: str = "ai_hunt"
    count: int = 3

class UpdatePostizConfigRequest(BaseModel):
    api_url: str
    api_key: Optional[str] = ""

@router.get("/queue")
def get_social_queue():
    posts = integrator.get_scheduled_posts()
    return {
        "status": "success",
        "total_queued": len(posts),
        "posts": posts
    }

@router.post("/auto-schedule")
def auto_schedule_daily_posts(payload: ScheduleRequest):
    try:
        scheduled = integrator.schedule_daily_batch_to_postiz(channel=payload.channel)
        return {
            "status": "success",
            "message": f"Successfully staged and scheduled {len(scheduled)} posts for @{payload.channel}",
            "scheduled_posts": scheduled
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
