from pydantic import BaseModel
class ProgressOverview(BaseModel): total_attempted: int; correct_answers: int; wrong_answers: int; overall_accuracy: float; tests_completed: int
