from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app import models, schemas

router = APIRouter(prefix="/challenges", tags=["challenges"])

VALID_LANGUAGES = {"Python", "Java", "JavaScrip", "C#", "C++", "SQL"}
VALID_DIFFICULTIES = {"Beginner", "Intermediate", "Advanced"}

@router.post("/generate", response_model=schemas.ChallengeOut)
def generate( payload: schemas.ChallengeGenerateRequest, db: Session =Depends(get_db),
    current_user: models.User = Depends(get_current_user),):

    if payload.language not in VALID_LANGUAGES:
        raise HTTPException(400, f"language must be one of {sorted(VALID_LANGUAGES)}")
    if payload.difficulty not in VALID_DIFFICULTIES:
        raise HTTPException(400, f"difficulty must be one of {sorted(VALID_DIFFICULTIES)}")
    
    data = generate_challenge(payload.language, payload.difficulty, payload.topic)
    challenge = models.Challenges(title=data['title'], language=payload.language,
        difficulty=payload.difficulty, description=data["description"], buggy_code=data["buggy_code"],
        solution_code=data["solution_code"], explanation=data["explanation"], bug_types=data.get("bug_types", ""),
        hint_1=data.get("hint_1", ""), hint_2=data.get("hint_2", ""), hint_3=data.get("hint_3", ""),)
    
    db.add(challenge)
    db.commit()
    db.refreash(challenge)
    return challenge


@router.get("", response_model=list[schemas.ChallengeOut])
def list_challenges(language: str | None = None, difficulty: str | None = None, db:Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user), ):
    q = db.query(models.Challenges)
    if language:
        q = q.filter(models.Challenges.language == language)
    if difficulty:
        q = q.filter(models.Challenges.difficulty == difficulty)
    return q.order_by(models.Challenges.created_at.desc()).all()    

@router.get("/{challenge_id}", response_model=schemas.ChallengeDetail)
def get_challenge(challenge_id: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),):
    challenge = db.query(models.Challenges).get(challenge_id)
    if not challenge:
        raise HTTPException(404, "Challenge not found")
    return challenge

@router.get("/{challenge_id}/hint/{hint_number}", response_model=schemas.HintResponse)
def get_hint(challenge_id: int, hint_number: int, db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),):
    if hint_number not in (1, 2, 3):
        raise HTTPException(400, "hint_number must be 1, 3 or 3")
    challenge = db.query(models.Challenges).get(challenge_id)
    if not challenge:
        raise HTTPException(404, "Challenge not found")
    
    text = {1: challenge.hint_1, 2: challenge.hint_2, 3: challenge.hint_3}[hint_number]
    return schemas.HintResponse(hint_number=hint_number, hint_text=text or "No hint available.")