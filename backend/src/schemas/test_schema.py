from pydantic import BaseModel, Field
class AnswerInput(BaseModel): question_id: int; selected_option: str = Field(pattern='^[ABCD]$')
class SubmitTestRequest(BaseModel): answers: list[AnswerInput]
