from pydantic import BaseModel
class TopicResponse(BaseModel): id: int; name: str; description: str | None; exam_category: str
