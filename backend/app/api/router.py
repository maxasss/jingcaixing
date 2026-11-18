from fastapi import APIRouter
from app.api.routes import admin_attractions, attractions, plans, routes
api_router = APIRouter(prefix="/api")
api_router.include_router(attractions.router)
api_router.include_router(plans.router)
api_router.include_router(routes.router)
api_router.include_router(admin_attractions.router)
