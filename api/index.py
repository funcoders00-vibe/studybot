import os
import sys

# Ensure backend directory and repository root are in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backend_dir = os.path.join(root_dir, "backend")

for path in [backend_dir, root_dir]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    try:
        from backend.src.main import app
    except ImportError:
        from src.main import app
except Exception as e:
    import traceback
    error_trace = traceback.format_exc()
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(title="StudyBot Root Startup Fallback")
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
                "error": "FastAPI Startup Failure on Vercel Root Entry",
                "detail": str(e),
                "traceback": error_trace.splitlines(),
            },
        )
