from fastapi import APIRouter
from ..models import Section, PydanticSection, PydanticSectionIn

router = APIRouter()

@router.get("/")
def readAll():
    return {"Hello": "World"}

@router.get("/")
def read():
    return {"Hello": "World"}

@router.post("/")
def post():
    return {"Hello": "World"}

@router.put("/")
def put():
    return {"Hello": "World"}