from fastapi import APIRouter
from pydantic import BaseModel
from database import movies_collection
from bson import ObjectId

router = APIRouter()

class Movie(BaseModel):
    title: str
    director: str
    year : int

@router.post("/add_movie")
def add_movie(movie: Movie):
    result = movies_collection.insert_one(movie.model_dump())
    return {"msg": "Movie added"}

@router.get("/movies")
def get_movies():
    movies = []
    for movie in movies_collection.find():
        movies.append({
            "id": str(movie["_id"]),
            "title": movie["title"],
            "director": movie["director"],
            "year" : movie["year"]
        })
    return movies



@router.delete("/delete")
def delete_movie(movie_id: str):
    result = movies_collection.delete_one({"_id": ObjectId(movie_id)})
    if result.deleted_count == 0:
        return {"msg:": "Movie not found"}
    return {"msg": "Movie deleted"}
