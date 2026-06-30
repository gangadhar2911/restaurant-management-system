from fastapi import Request
from fastapi.responses import JSONResponse


async def global_error_handler(request: Request, call_next):

    try:
        response = await call_next(request)
        return response

    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Internal Server Error"
            }
        )