import uvicorn
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print("==================================================================")
    print(f"  ⚡ OMNIVIRAL AI SAAS PLATFORM STARTED AT http://localhost:{port}  ")
    print("==================================================================")
    uvicorn.run("backend.app:app", host="127.0.0.1", port=port, reload=False)
