from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from backend.config import STATIC_DIR
from backend.database import init_db
from backend.routes.auth import router as auth_router
from backend.routes.ai_generator import router as ai_router
from backend.routes.subtitle_engine import router as subtitle_router
from backend.routes.digital_products import router as product_router
from backend.routes.billing import router as billing_router
from backend.routes.security_recon import router as recon_router
from backend.routes.analytics import router as analytics_router
from backend.routes.ai_hunt_channel import router as ai_hunt_router
from backend.routes.video_render_api import router as video_router
from backend.routes.postiz_social_api import router as social_router

app = FastAPI(
    title="OmniViral AI - Autonomous Video & Cashflow Platform",
    description="Production Micro-SaaS Engine for Automated AI Video Generation, Subtitle Styling, Digital Product Sales, and Swarm Intelligence.",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router)
app.include_router(ai_router)
app.include_router(subtitle_router)
app.include_router(product_router)
app.include_router(billing_router)
app.include_router(recon_router)
app.include_router(analytics_router)
app.include_router(ai_hunt_router)
app.include_router(video_router)
app.include_router(social_router)

# Mount frontend static directory
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="frontend")

@app.on_event("startup")
def on_startup():
    init_db()
