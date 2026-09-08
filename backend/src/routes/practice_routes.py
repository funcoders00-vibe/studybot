from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.schemas.practice_schema import StartPracticeRequest
from src.services.practice_services import start_practice
from src.utils.auth import get_current_user
router=APIRouter(prefix='/practice',tags=['practice'])
@router.post('/start')
def start(body:StartPracticeRequest,db:Session=Depends(get_db),user=Depends(get_current_user)):
    try: test=start_practice(db,user.id,body)
    except ValueError as error: raise HTTPException(404,str(error))
    return {'success':True,'message':'Practice started','data':{'test_id':test.id,'total_questions':test.total_questions,'status':test.status}}
