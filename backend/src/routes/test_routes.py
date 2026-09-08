from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.models.question_model import Question
from src.models.user_answer_model import UserAnswer
from src.repository.test_repository import get_owned_test,test_questions
from src.schemas.test_schema import SubmitTestRequest
from src.services.test_services import submit_test
from src.utils.auth import get_current_user
router=APIRouter(prefix='/tests',tags=['tests'])
def owned(db,id,user):
    test=get_owned_test(db,id,user.id)
    if not test: raise HTTPException(404,'Test not found')
    return test
@router.get('/{test_id}')
def get_test(test_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    test=owned(db,test_id,user); ids=[x.question_id for x in test_questions(db,test.id)]; questions=db.query(Question).filter(Question.id.in_(ids)).all()
    data=[{'id':q.id,'question_text':q.question_text,'option_a':q.option_a,'option_b':q.option_b,'option_c':q.option_c,'option_d':q.option_d,'difficulty':q.difficulty} for q in questions]
    return {'success':True,'message':'Test retrieved','data':{'id':test.id,'status':test.status,'questions':data}}
@router.post('/{test_id}/submit')
def submit(test_id:int,body:SubmitTestRequest,db:Session=Depends(get_db),user=Depends(get_current_user)): return {'success':True,'message':'Test submitted','data':submit_test(db,owned(db,test_id,user),body.answers)}
@router.get('/{test_id}/result')
def result(test_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    test=owned(db,test_id,user); answers=db.query(UserAnswer).filter_by(test_id=test.id).all(); correct=sum(x.is_correct for x in answers); total=test.total_questions
    return {'success':True,'message':'Result retrieved','data':{'total_questions':total,'correct_answers':correct,'wrong_answers':total-correct,'score_percentage':round(correct/total*100,2) if total else 0}}
@router.get('/{test_id}/review')
def review(test_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    test=owned(db,test_id,user); answers={x.question_id:x for x in db.query(UserAnswer).filter_by(test_id=test.id)}; ids=[x.question_id for x in test_questions(db,test.id)]; questions=db.query(Question).filter(Question.id.in_(ids)).all()
    return {'success':True,'message':'Review retrieved','data':[{'question':q.question_text,'options':{'A':q.option_a,'B':q.option_b,'C':q.option_c,'D':q.option_d},'selected_option':answers[q.id].selected_option,'correct_option':q.correct_option,'is_correct':answers[q.id].is_correct,'explanation':q.explanation,'source_book':q.source_book,'source_chapter':q.source_chapter,'source_page':q.source_page} for q in questions if q.id in answers]}
