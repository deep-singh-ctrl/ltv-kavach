"""
Main entry point for LTV-Kavach Server.
Serves the FastAPI backend and the interactive Single-Page Dashboard.
"""

import sys
import os

# Add local packages and project root to Python path
sys.path.insert(0, "/home/deepank-singh/Documents/ltv-kavach/packages")
sys.path.insert(0, "/home/deepank-singh/Documents/ltv-kavach")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from src.api import router

app = FastAPI(
    title="LTV-Kavach | Investor Resilience & Collateral Guardian",
    description="SEBI / NSDL SANGYAN Hackathon Investor Protection System for Loan Against Securities",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "online",
        "message": "LTV-Kavach API is live. Static UI index.html not yet initialized.",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"==================================================")
    print(f"🛡️  LTV-KAVACH INVESTOR RESILIENCE GUARDIAN")
    print(f"🚀  Running on: http://localhost:{port}")
    print(f"📚  API Documentation: http://localhost:{port}/docs")
    print(f"==================================================")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
