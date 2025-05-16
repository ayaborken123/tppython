from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
import models, schemas
from database import engine, get_db
import os
from dotenv import load_dotenv
import requests

models.Base.metadata.create_all(bind=engine)

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()

@app.post("/movies/", response_model=schemas.MoviePublic)
def create_movie(movie: schemas.MovieBase, db: Session = Depends(get_db)):
    db_movie = models.Movies(
        title=movie.title,
        year=movie.year,
        director=movie.director
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    for actor in movie.actors:
        db_actor = models.Actors(actor_name=actor.actor_name, movie_id=db_movie.id)
        db.add(db_actor)

    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/random/", response_model=schemas.MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
    movie = db.query(models.Movies).options(joinedload(models.Movies.actors)).order_by(func.random()).first()
    if not movie:
        raise HTTPException(status_code=404, detail="No movies found")
    return movie

@app.get("/ask-groq")
def ask_groq(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "gemma2-9b-it"  # Modèle mis à jour
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    return response.json()

@app.post("/generate_summary/", response_model=schemas.SummaryResponse)
def generate_summary(request: schemas.SummaryRequest, db: Session = Depends(get_db)):
    movie = db.query(models.Movies).options(joinedload(models.Movies.actors)).filter(models.Movies.id == request.movie_id).first()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    actor_names = ", ".join(actor.actor_name for actor in movie.actors)
    prompt_text = f"Generate a short, engaging summary for the movie '{movie.title}' ({movie.year}), directed by {movie.director} and starring {actor_names}."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "user", "content": prompt_text}],
        "model": "gemma2-9b-it"  # Modèle mis à jour
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to generate summary from Groq API")

    result = response.json()

    try:
        summary_text = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        summary_text = "No summary available"

    return {"summary_text": summary_text}
