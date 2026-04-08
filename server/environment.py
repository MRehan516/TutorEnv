import copy
import random
from typing import Optional
from models import (
    StudentProfile, TeachingAction,
    StepResult, ResetResult
)
from tasks import TASK_REGISTRY, create_task
from quiz import get_pre_quiz_score, get_topic_keywords

class TutorEnvironment:
    def __init__(self):
        self.student: Optional[StudentProfile] = None
        self.task_id: Optional[str] = None
        self.current_step: int = 0
        self.max_steps: int = 10
        self.total_reward: float = 0.0
        self.teaching_history: list = []
        self.example_used: bool = False
        self.questions_asked: int = 0

    def reset(self, task_id: str = "easy_vaccine_misconception") -> ResetResult:
        if task_id not in TASK_REGISTRY:
            raise ValueError(f"Unknown task: {task_id}")
        self.student = create_task(task_id)
        self.task_id = task_id
        self.current_step = 0
        self.max_steps = TASK_REGISTRY[task_id]["max_steps"]
        self.total_reward = 0.0
        self.teaching_history = []
        self.example_used = False
        self.questions_asked = 0

        return ResetResult(
            student_profile=copy.deepcopy(self.student),
            task_id=task_id,
            session_id="" 
        )

    def _validate_content(self, action: TeachingAction) -> bool:
        if not action.targets_misconception:
            return True
        keywords = get_topic_keywords(self.task_id)
        content_lower = action.content.lower()
        return any(k in content_lower for k in keywords)

    def step(self, action: TeachingAction) -> StepResult:
        if self.student is None:
            raise RuntimeError("Call reset() before step()")

        self.current_step += 1
        reward = 0.0

        if action.targets_misconception:
            if self._validate_content(action):
                reward += 0.35
            else:
                reward -= 0.10

        if action.action_type == "give_example":
            reward += 0.20
            self.example_used = True
            if self.student.learning_style == "example-based":
                reward += 0.10
        elif action.action_type == "ask_question":
            reward += 0.10
            self.questions_asked += 1
        elif action.action_type == "explain":
            reward += 0.10
        elif action.action_type == "check_understanding":
            reward += 0.05
        elif action.action_type == "summarize":
            if self.current_step >= self.max_steps - 2:
                reward += 0.15
            else:
                reward += 0.02

        if len(action.content) > 80:
            reward += 0.10

        if self.current_step == 4 and not self.example_used and self.student.learning_style == "example-based":
            reward -= 0.10

        reward = max(0.0, min(1.0, reward))
        self.total_reward += reward
        self.student.knowledge_level = min(1.0, self.student.knowledge_level + reward * 0.08)

        done = self.current_step >= self.max_steps
        post_quiz_score = None
        learning_gain = None

        if done:
            improvement = (self.student.knowledge_level - 0.25) * 0.85
            post_quiz_score = min(1.0, max(0.0, self.student.pre_quiz_score + improvement))
            self.student.post_quiz_score = post_quiz_score
            learning_gain = post_quiz_score - self.student.pre_quiz_score
            self.total_reward += max(-0.2, min(0.5, learning_gain * 1.5))

        avg_reward = self.total_reward / self.current_step if self.current_step > 0 else 0.0

        info = {
            "step": self.current_step,
            "total_reward": round(self.total_reward, 4),
            "average_reward": round(avg_reward, 4),
            "knowledge_level": round(self.student.knowledge_level, 4),
            "example_used": self.example_used,
            "questions_asked": self.questions_asked
        }

        if done:
            info["pre_quiz_score"] = round(self.student.pre_quiz_score, 4)
            info["post_quiz_score"] = round(post_quiz_score, 4)
            info["learning_gain"] = round(learning_gain, 4)

        return StepResult(
            student_profile=copy.deepcopy(self.student),
            reward=round(reward, 4),
            done=done,
            info=info
        )

    def state(self) -> StepResult:
        if self.student is None:
            raise RuntimeError("Call reset() before state()")

        avg_reward = self.total_reward / self.current_step if self.current_step > 0 else 0.0
        info = {
            "step": self.current_step,
            "total_reward": round(self.total_reward, 4),
            "average_reward": round(avg_reward, 4),
            "knowledge_level": round(self.student.knowledge_level, 4),
            "example_used": self.example_used,
            "questions_asked": self.questions_asked
        }
        return StepResult(
            student_profile=copy.deepcopy(self.student),
            reward=0.0,
            done=self.current_step >= self.max_steps,
            info=info
        )