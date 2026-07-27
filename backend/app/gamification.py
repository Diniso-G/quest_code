'''Small, self contained XP/level/streak/achievement logic used by the
submission router.'''
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import models

XP_BY_DIFFICULTY = {"Beginner": 10, "Intermediate": 25, "Advanced": 50}
XP_PER_LEVEL = 100

ACHIEVEMENT_DEFS = [
    ("FIRST_BUG_FIXED", "First Bug Fixed", "Fix your very first bug", "Crwn 1"),
    ("BUGS_100", "100 Bugs Solved", "Fix 100 bugs total", "Crwn 1"),
    ("SQL_MASTER", "SQL Master", "Solve 10 SQL challenges", "Crwn 1"),
    ("PYTHON DETECTIVE", "Python Detective", "Solve 10 Python challenges", "Crwn 1"),
    ("DEBUGGING_EXPERT", "Debugging Expert", "Reach Advanced difficulty and solve it correctly", "Crwn 1"),
    ("STREAK_30", "30-Day Streak", "Maintain a 30 day activity streak", "Crwn 1"),
]

def ensure_achievement_defs(db: Session):
    '''Seed the achievement table'''
    for code, title, desc, icon in ACHIEVEMENT_DEFS:
        exists = db.query(models.Achievement).filter_by(code=code).first()
        if not exists:
            db.add(models.Achievement(code=code, title=title, description=desc, icon=icon))

    db.commit()

def _award(db: Session, user:models.User, code:str, unlocked: list):
    achh = db.query(models.Achievement).filter_by(code=code).first()
    if not achh:
        return
    already = db.query(models.UserAchievement).filter_by(user_id=user.id, achievement_id=achh.id).first()
    if not already:
        db.add(models.UserAchievement(user_id=user.id, achievement_id=achh.id))
        unlocked.append(achh.title)

def update_streak(user: models.User):
    now = datetime.utcnow()
    if user.last_active_date is None:
        user.streak = 1
    else:
        delta = now.date() - user.last_active_date.date()
        if delta == timedelta(days=0):
            pass
        elif delta == timedelta(days=1):
            user.streak += 1
        else:
            user.streak = 1
    user.last_active_date = now

def apply_submission_result(
    db: Session, 
    user: models.User, 
    challenge: models.Challenges, 
    is_correct: bool,
    hints_used: int,
) -> tuple[int, list]:
    unlocked: list[str] = []
    xp_awarded = 0 

    if is_correct:
        base_xp = XP_BY_DIFFICULTY.get(challenge.difficulty, 10)
        penalty = min(hints_used, 3) * 0.15
        xp_awarded = max(1, round(base_xp * (1 - penalty)))

        user.xp += xp_awarded
        user.level = user.xp // XP_PER_LEVEL + 1
        user.bugs_fixed += 1
        user.challenges_com += 1
        update_streak(user)

        if user.bugs_fixed == 1:
            _award(db, user, "FIRST_BUG_FIXED", unlocked)
        if user.bugs_fixed >=100:
            _award(db, user, "BUGS_100", unlocked)
        if user.streak >=30:
            _award(db, user, "STREAK_30", unlocked)
        if challenge.difficulty == "Advanced":
            _award(db, user, "DEBUGGING_EXPERT", unlocked)

        if challenge.language.lower() == "sql":
            sql_solved = (
                db.query(models.Submission).join(models.Challenges).
                filter(models.Submission.user_id == user.id,
                    models.Submisson.is_correct ==True,
                    models.Challenges.language == "SQL",).count()
            )
            if sql_solved >= 10:
                _award(db, user, "SQL_MASTER", unlocked)

        if challenge.language.lower() == "python":
            py_solved = (
                db.query(models.Submission).join(models.Challenges).
                filter(models.Submission.user_id == user.id,
                    models.Submission.is_correct ==True,
                    models.Challenges.language == "Python",).count()
            )
            if py_solved >= 10:
                _award(db, user, "PYTHON_DETECTIVE", unlocked)

    db.commit()
    return xp_awarded, unlocked


