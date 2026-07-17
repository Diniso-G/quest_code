from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, SessionLocal
from app import models
from app.gamification import ensure_achievement_defs
from app.routers import auth, users, challenges

Base.metadata.create_all(bind=engine)

app = FastAPI( title="QuestCode", description="Learn programmin by finding real bugs. AI-generated coding challenges.",
    version="0.1.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(challenges.router)

@app.on_event("startup")
def seed_achievements():
    db = SessionLocal()
    try:
        ensure_achievement_defs(db)
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "ok", "service": "QuestCode backend"}
