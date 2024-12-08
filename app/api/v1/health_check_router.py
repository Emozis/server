from fastapi import APIRouter
import psutil
import time

from app.core import handle_exceptions
from app.utils.health_check import health_check


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get(
    path="",
    description="서버의 상태를 확인하는 health check endpoint"
)
@handle_exceptions
async def check_health():
    return health_check.get_system_health()

@router.get(
    path="/details",
    description="서버의 상세 상태를 확인하는 endpoint",
)
@handle_exceptions
async def check_health_details():
    cpu_stats = psutil.cpu_stats()
    memory = psutil.virtual_memory()

    return {
        "status": "healthy",
        "uptime": int(time.time() - health_check.start_time),
        "system_details": {
            "cpu": {
                "usage_percent": psutil.cpu_percent(),
                "count": psutil.cpu_count(),
                "context_switches": cpu_stats.ctx_switches,
                "interrupts": cpu_stats.interrupts
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "used": psutil.disk_usage('/').used,
                "free": psutil.disk_usage('/').free,
                "percent": psutil.disk_usage('/').percent
            }
        }
    }