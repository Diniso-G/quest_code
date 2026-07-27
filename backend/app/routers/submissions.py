from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app import models, schemas
from app.ai.code_reviewer import review_submission
from app.gamification import apply_submission_result

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("", response_model=schemas.SubmissionResult)
def submit_answer(payload: schemas.SubmissionCreate, hints_used: int = 0, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user),):
    challenge = db.query(models.Challenges).get(payload.challenge_id)
    if not challenge:
        raise HTTPException(404, "Challenge not found")

    review = review_submission(buggy_code=challenge.buggy_code, solution_code=challenge.solution_code, explanation=challenge.explanation, user_answer=payload.user_answer,)

    xp_awarded, unlocked = apply_submission_result(db, current_user, challenge, review["is_correct"], hints_used)

    submission = models.Submission(
        user_id=current_user.id,
        challenge_id=challenge.id,
        user_answer=payload.user_answer,
        is_correct=review["is_correct"],
        ai_feedback=review["feedback"],
        ai_score=review["score"],
        hints_used=hints_used,
        xp_awarded=xp_awarded,)

    db.add(submission)
    db.commit()

    return schemas.SubmissionResult(
        is_correct=review["is_correct"],
        ai_score=review["score"],
        ai_feedback=review["feedback"],
        correct_solution=challenge.solution_code,
        explanation=challenge.explanation,
        xp_awarded=xp_awarded,
        new_level=current_user.level,
        new_xp=current_user.xp,
        new_streak=current_user.streak,
        achievements_unlocked=unlocked,
    )

@router.get("/history", response_model=list[schemas.SubmissionResult])
def my_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    subs = (db.query(models.Submission).filter(models.Submission.user_id == current_user.id).order_by(models.Submission.created_at.desc()).all())

    out = []
    for s in subs:
        out.append(schemas.SubmissionResult(
            is_correct=s.is_correct,
            ai_score=s.ai_score or 0,
            ai_feedback=s.ai_feedback or "",
            correct_solution=s.challenge.solution_code,
            explanation=s.challenge.explanation,
            xp_awarded=s.xp_awarded,
            new_level=current_user.level,
            new_xp=current_user.xp,
            new_streak=current_user.streak,
            achievements_unlocked=[],
        ))
    return out