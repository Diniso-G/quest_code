import json
import difflib
from app.ai.client import ai_available, chat

SYSTEM_PROMPT = """You are an expert code reviewer grading a student's attempt to fix a buggy piece
of code on QUEST CODE. Your will be given be given the original buggy code, the canonical fixed solution, 
the explanation of the bugs, and the student's submitted answer (which may be a fixed code snippet, a written
explanation, or both).

Grade fairly: the student does not need to match the canonical solution word for word, they need to have correctly
identified and fixed the actual bug(s).

Respond with ONLY a JSON object with these exact keys:
{
    "is_correct": true or false,
    "score": a number from 0 to 100,
    "feedback": "specific, encouraging feedback: what they got right, what's missing or still wrong, and one professional tip"

}
No prose outside the JSON.
"""

def review_submission(buggy_code: str, solution_code: str, explanation: str, user_answer: str) -> dict:
    if ai_available:
        user_prompt = (
            f"BUGGY CODE:\n{buggy_code}\n\n"
            f"CANONICAL FIX:\n{solution_code}\n\n"
            f"BUG EXPLANATION:\n{explanation}\n\n"
            f"STUDENT ANSWER:\n{user_answer}\n\n"
        )
        raw = chat(SYSTEM_PROMPT, user_prompt, json_mode=True)
        data = json.loads(raw)
        return {
            "is_correct": bool(data.get("is_correct")),
            "score": float(data.get("score", 0)),
            "feedback": data.get("feedback", ""),
        }

    ratio = difflib.SequenceMatcher(None, user_answer.strip(), solution_code.strip()).ratio()
    score = round(ratio * 100, 1)
    is_correct = score >= 60
    if is_correct:
        feedback = ("Nice work. Your fix lines up closely with the canonical solution. Re-read the explanation to make sure you understand *why* it works, not just what changed.")
    else:
        feedback = ("Your answer doesn't closly match the expected fix yet. Re-read the bug explanation, compare your code line-by-line against the buggy version, and tru again.")
    return {"is_correct": is_correct, "score": score, "feedback": feedback}