from fastapi import FastAPI
from . import models
from .database import engine, SessionLocal
from .routers import post, user, auth, vote
from .config import settings

#models.Base.metadata.create_all(bind=engine) -- was needed for sqlalchemy before alembic
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message" : "Hellow piipl"}
