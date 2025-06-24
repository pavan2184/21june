from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import movies_collection
from bson import ObjectId
from .authentication import get_current_user

router = APIRouter()

class Movie(BaseModel):
    title: str
    director: str
    year : int

@router.post("/add_movie")
def add_movie(movie: Movie, current_user: str = Depends(get_current_user)):
    result = movies_collection.insert_one(movie.model_dump())
    return {
        "msg": "Movie added",
        "added_by": current_user  
    }

@router.get("/movies")
def get_movies(current_user: str = Depends(get_current_user)):
    movies = []
    for movie in movies_collection.find():
        movies.append({
            "id": str(movie["_id"]),
            "title": movie["title"],
            "director": movie["director"],
            "year": movie["year"]
        })
    return {
        "user": current_user,  
        "movies": movies
    }


@router.delete("/delete")
def delete_movie(name: str):
    result = movies_collection.delete_one({"title": name})
    if result.deleted_count == 0:
        return {"msg:": "Movie not found"}
    return {"msg": "Movie deleted"}
