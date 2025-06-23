from fastapi import APIRouter
from pydantic import BaseModel
from database import movies_collection
from bson import ObjectId

router = APIRouter()

class Movie(BaseModel):
    title: str
    director: str

@router.post("/add_movie")
def add_movie(movie: Movie):
    result = movies_collection.insert_one(movie.model_dump())
    return {"id": str(result.inserted_id), "msg": "Movie added"}

@router.get("/movies")
def get_movies():
    movies = []
    for movie in movies_collection.find():
        movies.append({
            "id": str(movie["_id"]),
            "title": movie["title"],
            "director": movie["director"]
        })
    return movies

@router.put("/update_movie/{movie_id}")
def update_movie(movie_id: str, updated_movie: Movie):
    result = movies_collection.update_one(
        {"_id": ObjectId(movie_id)},
        {"$set": updated_movie.model_dump()}
    )
    if result.matched_count == 0:
        return {"msg:": "Movie not found"}
    return {"msg": "Movie updated"}

@router.delete("/delete_movie/{movie_id}")
def delete_movie(movie_id: str):
    result = movies_collection.delete_one({"_id": ObjectId(movie_id)})
    if result.deleted_count == 0:
        return {"msg:": "Movie not found"}
    return {"msg": "Movie deleted"}
