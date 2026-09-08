from fastapi import APIRouter, Depends, Response, Cookie
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.schemas.login_schema import LoginRequest
from src.services.login_services import login
from src.repository.login_repository import deactivate_session
from src.settings import settings
from src.utils.auth import get_current_user
router=APIRouter(prefix='/auth',tags=['auth'])
@router.post('/login')
def login_route(body:LoginRequest,response:Response,db:Session=Depends(get_db)):
    user,session=login(db,body.email,body.password); response.set_cookie(settings.session_cookie_name,session.session_token,httponly=True,secure=settings.secure_cookies,samesite='lax',max_age=settings.session_expire_hours*3600); return {'success':True,'message':'Login successful','data':{'user':{'id':user.id,'name':user.name,'email':user.email}}}
@router.post('/logout')
def logout(response:Response,token:str|None=Cookie(default=None,alias=settings.session_cookie_name),db:Session=Depends(get_db)):
    if token: deactivate_session(db,token)
    response.delete_cookie(settings.session_cookie_name); return {'success':True,'message':'Logged out successfully'}
@router.get('/me')
def me(user=Depends(get_current_user)): return {'success':True,'message':'Authenticated user','data':{'user':{'id':user.id,'name':user.name,'email':user.email}}}
