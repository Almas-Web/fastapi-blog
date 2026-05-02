import os

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from apis.base import api_router
from db.base import Base
from db.models.user import User
from repositories.user import UserRepository   
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME, 
    version=settings.PROJECT_VERSION
)

# create folder automatically if not exists
os.makedirs("uploads/images", exist_ok=True)


app.mount("/static",StaticFiles(directory="uploads/images"),name="static")

app.include_router(api_router)

#list of allowed origins you can add specific domains or '*' for all origins
origins = [
    "http://localhost:3000",  # Frontend during development
    "http://your_frontend_domain.com",  # Production frontend
]

# Adding CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def hello_api():
    print(settings.DATABASE_URL)
    return {"message": "Hello World"}

@app.get("/protected")
async def protected_route(current_user:User=Depends(UserRepository.get_current_user)):
    return{"message":f"Hello{current_user.email},you are authorized"}