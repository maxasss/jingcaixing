from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api.router import api_router
from app.core.exceptions import BusinessError, business_error_handler
app = FastAPI(title="京彩行旅行智能规划系统")
app.add_exception_handler(BusinessError, business_error_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
app.mount("/images", StaticFiles(directory=Path(__file__).resolve().parents[2] / "static" / "images"), name="images")
@app.get("/api/health")
def health(): return {"code": 0, "message": "ok", "data": {"status": "ok"}}
