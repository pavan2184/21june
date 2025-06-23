from fastapi import FastAPI
from routes import authentication, get_movielist

app = FastAPI()

app.include_router(authentication.router)
app.include_router(get_movielist.router)