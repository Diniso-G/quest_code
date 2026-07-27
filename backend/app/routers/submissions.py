from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app import models, schemas
from app.ai.code_reviewer import review_submission
from app.gamification import apply_submission_result

router = APIRouter(prefix="/submissions", tags=["submissions"])

@router.post("", response_model=schemas.SubmissionResults)