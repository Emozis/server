import psutil
import time


class HealthCheck:
    def __init__(self):
        self.start_time = time.time()

    def get_system_health(self) -> dict:
        return {
            "status": "healthy",
            "uptime": int(time.time() - self.start_time),  # 서버 가동 시간(초)
            "system_info": {
                "cpu_usage": f"{psutil.cpu_percent()}%",
                "memory_usage": f"{psutil.virtual_memory().percent}%",
                "disk_usage": f"{psutil.disk_usage('/').percent}%"
            }
        }

health_check = HealthCheck()