from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.database import Base,engine
from src.settings import settings
from src.routes import login_routes, topic_routes, practice_routes, mock_test_routes, test_routes, revision_routes, progress_routes, chat_routes
import src.models
app = FastAPI(title=settings.app_name)
allowed_origins = list({settings.frontend_url, 'http://localhost:5173', 'http://127.0.0.1:5173'})
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
for router in [login_routes.router, topic_routes.router, practice_routes.router, mock_test_routes.router, test_routes.router, revision_routes.router, progress_routes.router, chat_routes.router]:
    app.include_router(router, prefix='/api/v1')
@app.on_event('startup')
def startup(): Base.metadata.create_all(bind=engine)
@app.get('/health')
def health(): return {'status':'healthy'}
