from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.schemas.mock_test_schema import StartMockTestRequest
from src.services.mock_test_services import start_mock_test
from src.utils.auth import get_current_user
router=APIRouter(prefix='/mock-tests',tags=['mock tests'])
@router.post('/start')
def start(body:StartMockTestRequest,db:Session=Depends(get_db),user=Depends(get_current_user)):
    try: test=start_mock_test(db,user.id,body)
    except ValueError as error: raise HTTPException(404,str(error))
    return {'success':True,'message':'Mock test started','data':{'test_id':test.id,'total_questions':test.total_questions,'duration_minutes':test.duration_minutes,'status':test.status}}
