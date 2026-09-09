import os
import sys

# Ensure backend root directory is in sys.path so 'src' and other modules import cleanly on Vercel
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from src.main import app
except Exception as e:
    import traceback
    error_trace = traceback.format_exc()
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(title="StudyBot Startup Fallback")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    async def fallback_error_handler(full_path: str):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "FastAPI Startup Failure on Vercel",
                "detail": str(e),
                "traceback": error_trace.splitlines(),
            },
        )