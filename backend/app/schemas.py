from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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

