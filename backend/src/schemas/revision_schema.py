from pydantic import BaseModel, Field
class StartRevisionRequest(BaseModel): topic_id: int; number_of_questions: int = Field(ge=1, le=50)
