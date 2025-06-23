from fastapi import APIRouter

router = APIRouter()

@router.get("/profile")
def get_profile():
    return {"msg": "User profile route is working!"}