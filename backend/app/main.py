from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.exceptions import BusinessError, business_error_handler
app = FastAPI(title="京彩行旅行智能规划系统")
app.add_exception_handler(BusinessError, business_error_handler)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router)
@app.get("/api/health")
def health(): return {"code": 0, "message": "ok", "data": {"status": "ok"}}
