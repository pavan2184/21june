from fastapi import FastAPI
from routes.authentication import router as auth_router
from routes.get_movielist import router as movie_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(movie_router, prefix="/movies", tags=["Movies"])
