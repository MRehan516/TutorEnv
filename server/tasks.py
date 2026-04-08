import random
from models import StudentProfile
from quiz import get_pre_quiz_score

TASK_REGISTRY = {
    "easy_vaccine_misconception": {
        "topic": "How vaccines work",
        "misconception": "Vaccines contain live viruses that cause the disease they prevent",
        "misconception_strength": 0.8,
        "knowledge_level": 0.25,
        "learning_style": "example-based",
        "difficulty": "easy",
        "description": (
            "Student believes vaccines give you the disease. "
            "Agent must correct this misconception using examples "
            "and clear explanation of how immune memory works."
        ),
        "max_steps": 8
    },
    "medium_compound_interest": {
        "topic": "How compound interest works",
        "misconception": "Compound interest earns the same amount each year as simple interest",
        "misconception_strength": 0.7,
        "knowledge_level": 0.35,
        "learning_style": "verbal",
        "difficulty": "medium",
        "description": (
            "Student thinks compound and simple interest are identical. "
            "Agent must demonstrate the exponential growth difference "
            "using clear verbal explanation and numbers."
        ),
        "max_steps": 10
    },
    "hard_evolution_misconception": {
        "topic": "How evolution works",
        "misconception": "Animals evolve intentionally because they need a new trait to survive",
        "misconception_strength": 0.9,
        "knowledge_level": 0.2,
        "learning_style": "example-based",
        "difficulty": "hard",
        "description": (
            "Student holds the deeply ingrained intentionality misconception "
            "about evolution. Agent must explain natural selection, random "
            "mutation, and generational timescales. Hardest to correct."
        ),
        "max_steps": 12
    }
}


def create_task(task_id: str) -> StudentProfile:
    if task_id not in TASK_REGISTRY:
        raise ValueError(
            f"Unknown task: {task_id}. "
            f"Valid tasks: {list(TASK_REGISTRY.keys())}"
        )
    config = TASK_REGISTRY[task_id]
    pre_score = get_pre_quiz_score(
        config["topic"],
        config["misconception_strength"]
    )
    return StudentProfile(
        student_id=f"S_{task_id[:4].upper()}",
        topic=config["topic"],
        misconception=config["misconception"],
        knowledge_level=config["knowledge_level"],
        learning_style=config["learning_style"],
        pre_quiz_score=pre_score,
        post_quiz_score=None
    )