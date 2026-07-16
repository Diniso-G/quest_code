from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base, SessionLocal
from app import models
from app.routers import auth, users

Base.metadata.create_all(bind=engine)

app = FastAPI( title="QuestCode", description="Learn programmin by finding real bugs. AI-generated coding challenges.",
    version="0.1.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "QuestCode backend"}
