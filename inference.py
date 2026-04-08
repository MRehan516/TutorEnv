import os
import json
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy_token")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

BASE_URL = "http://127.0.0.1:8000"
TASKS = ["easy_vaccine_misconception", "medium_compound_interest", "hard_evolution_misconception"]

def run_agent():
    for task in TASKS:
        print(f"[START] Task: {task}")

        res = httpx.post(f"{BASE_URL}/reset", json={"task_id": task})
        if res.status_code != 200:
            print(f"Failed to reset: {res.text}")
            continue

        session = res.json()
        student = session["student_profile"]
        done = False
        step_count = 0

        while not done and step_count < 15:
            step_count += 1

            prompt = f"""
            You are an AI tutor. The student's current misconception is: '{student['misconception']}'.
            Their knowledge level is {student['knowledge_level']} (0.0 to 1.0).
            Choose a teaching action to correct this.
            Respond strictly in valid JSON format with the following keys:
            - action_type (string): must be one of ["explain", "give_example", "ask_question", "check_understanding", "summarize"]
            - content (string): what you say to the student
            - targets_misconception (boolean): true or false
            """

            # Using the required OpenAI client format
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            action_data = json.loads(response.choices[0].message.content)

            step_res = httpx.post(f"{BASE_URL}/step", json=action_data)
            result = step_res.json()

            student = result["student_profile"]
            reward = result["reward"]
            done = result["done"]
            info = result["info"]

            print(f"[STEP] Step: {step_count} | Action: {action_data['action_type']} | Reward: {reward}")

        final_score = info.get('learning_gain', info.get('total_reward', 0.0))
        print(f"[END] Task: {task} | Score: {final_score}")

if __name__ == "__main__":
    run_agent()
