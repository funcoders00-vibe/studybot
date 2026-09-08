from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.services.progress_services import overview_data,topics_data
from src.utils.auth import get_current_user
router=APIRouter(prefix='/progress',tags=['progress'])
@router.get('/overview')
def overview(db:Session=Depends(get_db),user=Depends(get_current_user)): return {'success':True,'message':'Progress retrieved','data':overview_data(db,user.id)}
@router.get('/topics')
def topics(db:Session=Depends(get_db),user=Depends(get_current_user)): return {'success':True,'message':'Topic performance retrieved','data':topics_data(db,user.id)}
@router.get('/weak-topics')
def weak(db:Session=Depends(get_db),user=Depends(get_current_user)):
    return {'success':True,'message':'Weak topics retrieved','data':[x for x in topics_data(db,user.id) if x['total_attempted']>=5 and x['accuracy_percentage']<60]}
