from fastapi import FastAPI

from app.database import engine, Base, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI( title="QuestCode", description="Learn programmin by finding real bugs. AI-generated coding challenges.",
    version="0.1.0",
)

@app.get("/")
def root():
    return {"status": "ok", "service": "QuestCode backend"}
