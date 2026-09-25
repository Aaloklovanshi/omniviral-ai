from fastapi import APIRouter
from backend.services.ai_hunt_engine import AIHuntEngine

router = APIRouter(prefix="/api/ai-hunt", tags=["ai_hunt"])
engine = AIHuntEngine()

@router.get("/daily-pack")
def get_daily_ai_hunt_pack(count: int = 3):
    packs = engine.generate_daily_ai_hunt_pack(count=count)
    return {
        "status": "success",
        "channel": "@ai_hunt",
        "total_generated": len(packs),
        "packs": packs
    }
