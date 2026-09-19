from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def _validate_email(v: str) -> str:
    if not EMAIL_RE.match(v):
        raise ValueError("invalid email format")
    return v


class UserCreate(BaseModel):
    email: str
    username: str
    password: str = Field(min_length=8)

    _validate_email = field_validator("email")(_validate_email)

class UserLogin(BaseModel):
    email: str
    password: str

    _validate_email = field_validator("email")(_validate_email)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    xp: int
    level: int
    streak: int
    challenges_com: int
    bugs_fixed: int
    
    class Config:
        from_attributes = True

class ChallengeGenerateRequest(BaseModel):
    language: str
    difficulty: str
    topic: Optional[str] = None

class ChallengeOut(BaseModel):
    id: int
    title: str
    language: str
    difficulty: str
    description: str
    buggy_code: str
    bug_types: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ChallengeDetail(ChallengeOut):

    pass

class HintResponse(BaseModel):
    hint_number: int
    hint_text: str

class SubmissionCreate(BaseModel):
    challenge_id: int
    user_answer: str

class SubmissionResult(BaseModel):
    is_correct: bool
    ai_score: float
    ai_feedback: str
    correct_solution: str
    explanation: str
    xp_awarded: int
    new_level: int
    new_xp: int
    new_streak: int
    achievements_unlocked: List[str] = []
    

class DashboardStats(BaseModel):
    xp: int
    level: int
    streak: int
    challenges_com: int
    bugs_fixed: int
    xp_to_next_level: int
    achievements: List[str]

class HistoryItem(BaseModel):
    submission_id: int
    challenge_id: int
    challenge_title: str
    difficulty: str
    language: str
    is_correct: bool
    xp_awarded: int
    created_at: datetime

    class Config:
        from_attributes = True

