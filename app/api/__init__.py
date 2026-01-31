"""API routes initialization."""
from fastapi import APIRouter
from .files import router as files_router
from .simulation import router as simulation_router

api_router = APIRouter()

# Include sub-routers
api_router.include_router(files_router, tags=["files"])
api_router.include_router(simulation_router, tags=["simulation"])

__all__ = ["api_router"]
