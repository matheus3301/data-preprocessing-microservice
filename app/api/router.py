from fastapi import APIRouter

from app.api.v1.endpoints import process

router = APIRouter()

router.include_router(process.router, prefix="/v1", tags=["process"]) 