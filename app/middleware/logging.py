import time
from datetime import datetime

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        log_data = {
            "time": datetime.utcnow().isoformat(),
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time": round(process_time, 4),
            "client_ip": request.client.host
        }

        print("[LOG]", log_data)

        return response