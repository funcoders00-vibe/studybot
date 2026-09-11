import os
from fastapi import APIRouter, Cookie, Depends, Request, Response
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.schemas.login_schema import LoginRequest
from src.services.login_services import login
from src.repository.login_repository import deactivate_session
from src.settings import settings
from src.utils.auth import get_current_user

router = APIRouter(prefix='/auth', tags=['auth'])


def _get_cookie_security_params(request: Request | None = None):
    # Cross-origin requests between different domains (e.g. Vercel) require SameSite=None and Secure=True
    origin = request.headers.get('origin', '') if request else ''
    is_vercel = os.getenv('VERCEL') == '1' or 'vercel.app' in origin or 'vercel.app' in settings.frontend_url
    is_cross_origin = settings.environment.lower() == 'production' or is_vercel or origin.startswith('https://')
    samesite = 'none' if is_cross_origin else 'lax'
    secure = True if is_cross_origin else settings.secure_cookies
    return samesite, secure


@router.post('/login')
def login_route(body: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    user, session = login(db, body.email, body.password)
    samesite, secure = _get_cookie_security_params(request)

    response.set_cookie(
        key=settings.session_cookie_name,
        value=session.session_token,
        httponly=True,
        secure=secure,
        samesite=samesite,
        max_age=settings.session_expire_hours * 3600,
        path='/'
    )
    return {
        'success': True,
        'message': 'Login successful',
        'data': {
            'token': session.session_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }
    }


@router.post('/logout')
def logout(
    request: Request,
    response: Response,
    token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
    db: Session = Depends(get_db)
):
    auth_token = token
    auth_header = request.headers.get('Authorization') or request.headers.get('authorization')
    if auth_header and auth_header.startswith('Bearer '):
        auth_token = auth_header[7:].strip()
    elif request.headers.get('x-session-token'):
        auth_token = request.headers.get('x-session-token')

    if auth_token:
        deactivate_session(db, auth_token)
    samesite, secure = _get_cookie_security_params(request)
    response.delete_cookie(
        key=settings.session_cookie_name,
        samesite=samesite,
        secure=secure,
        path='/'
    )
    return {'success': True, 'message': 'Logged out successfully'}


@router.get('/me')
def me(user = Depends(get_current_user)):
    return {
        'success': True,
        'message': 'Authenticated user',
        'data': {
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        }
    }
