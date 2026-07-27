import json
import random
from app.ai.client import ai_available, chat

SYSTEM_PROMPT = """You are an expert software engineering instructor who
designs bug-hunting exercises for QUEST CODE, a platform that teaches developers
to read and debug real code instead of solving abstract algorithm puzzles.

Given a programming language, a difficulty level and an optional topic, you must
invent ONE realistic, self-contained code snippet that LOOKS like it belongs in a
real project (a function, a class, or small module) and contains 1-3 intentional
bugs appropriate for the requested difficulty (syntax, logic, performance, or 
security bugs such as SQL injection, XSS, or race conditions).


Respond with ONLY a JSON object with these exact keys:
{
    "title": "short descriptive title",
    "description": "1-3 sentences describing what the code is supposed to do and what the user must find",
    "buggy_code": "the full code snippet, wuth real bugs, no comments pointing them out",
    "solution_code": "the corrected version of the same code",
    "explanation": "clear explanation of every bug, why it's wrong, and why the fix works",
    "bug_types": "comma-seperated tags, e.g. logic-error, off-by-one",
    "hint_1": "a small clue pointing at the general area of the bug",
    "hint_2": "a bigger clue narrowing down the exact line/cause",
    "hint_3": "an almost-complete explanation of the bug, without giving the fixed code verbatim"
}
No prose outside the JSON.
"""

_FALLBACK_BANK = [
    {
        "title": "Off-by-one in pagination",
        "language": "Python",
        "difficulty": "Beginner",
        "description": "This function is suppose to return the items for a given page, but callers report the last item of each page is missing.",

        "buggy_code": (
            "def get_page(items, page, page_size=10):\n"
            "   start = page * page_size\n"
            "   end = start + page_size - 1\n"
            "   return items[start:end]\n"
        ),
        "solution_code": (
            "def get_page(items, page, page_size=10):\n"
            "   start = page * page_size\n"
            "   end = start + page_size\n"
            "   return items[start:end]\n"
        ),
        "explanation": "Python slicing is already exclusive of the end index, so subtracting 1 from `end` drops the last item of every page. `items[start:end]` with `end = start + page_size` already returns the correct number of items.",

        "bug_types": "off-by-one, logic-error",
        "hint_1": "Look closely at how `end` is calculated.",
        "hint_2": "Remember how Python list slicing handles its end index.",
        "hint_3": "Slicing is exclusive of `end`, so subtracting 1 removes one item too many from every page.",

    },

    {
        "title": "SQL injection in user lookup",
        "language": "SQL",
        "difficulty": "Intermediate",
        "description": "This function builds a query to look up a username. Security review flagged it as unsafe.",
    
        "buggy_code": (
            "def get_user(cursor, username):\n"
                "   query = \"SELECT * FROM users WHERE username = '\" + username + \"'\"\n"
                "   cursor.execute(query)\n"
                "   return cursor.fetchone()\n"
        ),
        "solution_code": (
            "def get_user(cursor, username):\n"
                "   query = \"SELECT * FROM users WHERE username = %s\"\n"
                "   cursor.execute(query, (username,))\n"
                "   return cursor.fetchone()\n"
        ),
        "explanation": "String-concatenating user input directly into SQL allows an attacker to inject arbitrary SQL (e.g. `' OR '1'='1`). Using parameterized queries lets the database driver safely escapte the value.",
    
        "bug_types": "security, sql-injection",
        "hint_1": "Think about what happens if `username` contains a quote character.",
        "hint_2": "The query string is built with a plain string concatenation of user input.",
        "hint_3": "This is a classic SQL injection vulnerability; parameterized queries fix it.",
    
    },

    {
        "title": "Race condition in counter increment",
        "language": "Java",
        "difficulty": "Advanced",
        "description": "Under concurrent load, this shared request counter sometimes undercounts requests compared to the true number of calls.",
    
        "buggy_code": (
            "public class RequestCounter {\n"
            "   private int count = 0;\n"
            "   public void increment() {\n"
            "       count = count + 1;\n"
            "   }\n"
            "   public int get() {\n"
            "       return count;\n"
            "   }\n"
            "}\n"
        ),
        "solution_code": (
            "import java.util.concurrent.atomic.AtomicInteger;\n\n"
            "public class RequestCounter {\n"
            "   private final AtomicInteger count = new AtomicInteger(0);\n"
            "   public void increment() {\n"
            "       count.incrementAndGet();\n"
            "   }\n"
            "   public int get() {\n"
            "       return count.get();\n"
            "   }\n"
            "}\n"
        ),
        "explanation": "`count = count + 1` is a read-modify-write sequence that isn't atomic. Two threads can read the same values before either writes back, losing an increment. `AtomicIntger` (or `synchronized`) makes the operation atomic",
    
        "bug_types": "concurrency, race-condition",
        "hint_1": "Consider what happens if two threads call `increment()` at the exact same time.",
        "hint_2": "`count = count + 1` is not a single atomic CPU instruction.",
        "hint_3": "Use `AtomicInteger` or synchronize the method to make the increment atomic.",
    
    }
    
]

def generate_challenge(language: str, difficulty: str, topic: str | None = None) -> dict:
    if ai_available:
        user_prompt = f"Language: {language}\nDifficulty: {difficulty}\n"
        if topic:
            user_prompt += f"Topic focus: {topic}\n"
        raw = chat(SYSTEM_PROMPT, user_prompt, json_mode=True)
        data = json.loads(raw)
        data["language"] = language
        data["difficulty"] = difficulty
        return data

    matches = [c for c in _FALLBACK_BANK if c["language"].lower() == language.lower()]
    if not matches:
        matches = _FALLBACK_BANK
    chosen = dict(random.choice(matches))
    chosen["language"] = language
    chosen["difficulty"] = difficulty
    return chosen