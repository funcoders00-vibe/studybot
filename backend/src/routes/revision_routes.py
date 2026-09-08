from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.schemas.revision_schema import StartRevisionRequest
from src.services.revision_services import get_wrong_answers,start_revision
from src.utils.auth import get_current_user
router=APIRouter(prefix='/revision',tags=['revision'])
@router.get('/wrong-answers')
def wrong_answers(topic_id:int|None=None,limit:int=10,db:Session=Depends(get_db),user=Depends(get_current_user)):
    rows=get_wrong_answers(db,user.id,topic_id,limit); return {'success':True,'message':'Wrong answers retrieved','data':[{'question_id':q.id,'question_text':q.question_text,'wrong_count':w.wrong_count,'topic_id':q.topic_id} for q,w in rows]}
@router.post('/start')
def start(body:StartRevisionRequest,db:Session=Depends(get_db),user=Depends(get_current_user)):
    test=start_revision(db,user.id,body); return {'success':True,'message':'Revision started','data':{'test_id':test.id,'total_questions':test.total_questions}}
