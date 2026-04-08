from pydantic import BaseModel
from typing import Optional, List


class StudentProfile(BaseModel):
    student_id: str
    topic: str
    misconception: str
    knowledge_level: float
    learning_style: str
    pre_quiz_score: float
    post_quiz_score: Optional[float] = None


class TeachingAction(BaseModel):
    action_type: str
    content: str
    targets_misconception: bool


class StepResult(BaseModel):
    student_profile: StudentProfile
    reward: float
    done: bool
    info: dict


class ResetResult(BaseModel):
    student_profile: StudentProfile
    task_id: str
    session_id: str


class QuizResult(BaseModel):
    score: float
    answers: List[dict]
    learning_gain: float


class TaskInfo(BaseModel):
    task_id: str
    description: str
    difficulty: str
    topic: str
    misconception: str
    max_steps: int