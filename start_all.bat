@echo off
TITLE OmniViral AI - Autonomous Money System & SaaS
echo ==================================================================
echo   🚀 STARTING OMNIVIRAL AI FULL-STACK SAAS & 20-AGENT SWARM
echo ==================================================================

cd /d "%~dp0"

echo [*] Running 20-Agent Autonomous Revenue Swarm...
python agents\orchestrator.py

echo.
echo [*] Launching OmniViral Web SaaS Server on http://localhost:8000...
python start_server.py

pause
