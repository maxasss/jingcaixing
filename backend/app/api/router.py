from fastapi import APIRouter
from app.api.routes import attractions, plans, routes
api_router = APIRouter(prefix="/api")
api_router.include_router(attractions.router)
api_router.include_router(plans.router)
api_router.include_router(routes.router)
