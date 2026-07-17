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
    buy_types: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ChallengeDetail(ChallengeOut):

    pass

class HintResponse(BaseModel):
    hint_number: int
    hint_text: str




class DashboardStats(BaseModel):
    xp: int
    level: int
    streak: int
    challenges_com: int
    bugs_fixed: int
    xp_to_next_level: int
    achievements: List[str]

