from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.repository.topic_repository import list_topics,get_topic
from src.utils.auth import get_current_user
router=APIRouter(prefix='/topics',tags=['topics'])
@router.get('')
def topics(db:Session=Depends(get_db),_=Depends(get_current_user)): return {'success':True,'message':'Topics retrieved','data':[{'id':x.id,'name':x.name,'description':x.description,'exam_category':x.exam_category} for x in list_topics(db)]}
@router.get('/{topic_id}')
def topic(topic_id:int,db:Session=Depends(get_db),_=Depends(get_current_user)):
    item=get_topic(db,topic_id)
    if not item: raise HTTPException(404,'Topic not found')
    return {'success':True,'message':'Topic retrieved','data':{'id':item.id,'name':item.name,'description':item.description,'exam_category':item.exam_category}}
