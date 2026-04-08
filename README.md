# TutorEnv - Meta OpenEnv Hackathon

TutorEnv is an OpenEnv-compliant environment designed to train AI tutors. The agent's objective is to interact with a simulated student, identify their misconceptions, and take teaching actions to correct them. The environment calculates reward based on the student's *learning gain* (post-quiz score minus pre-quiz score).

## Setup & Local Testing
1. Create virtual environment: `python -m venv .venv`
2. Activate: `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
3. Install dependencies: `pip install -r requirements.txt`
4. Run server: `uvicorn app:app --reload`
5. Run test agent: `python inference.py`

## OpenEnv Compatibility
This environment complies with the Meta OpenEnv specification. It exposes `/reset` and `/step` endpoints and is packaged with a standard `openenv.yaml` and `Dockerfile`.