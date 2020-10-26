from typing import List, Dict
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator
from models import Cours

PydanticCours = pydantic_model_creator(Cours, name='Cours')
PydanticCoursIn = pydantic_model_creator(Cours, name='CoursIn', exclude_readonly=True)

class CoursBaseIn(PydanticCoursIn):
    cours_id: int
    teacher_id: int

    class Config:
        orm_mode = True

class CoursBaseOut(PydanticCours):
    cours_id: int
    teacher_id: int

    class Config:
        orm_mode = True

router = APIRouter()

@router.get("/", response_model=List[CoursBaseOut])
async def read():
	return await CoursBaseOut.from_queryset(Cours.all())

@router.get("/{id}", response_model=CoursBaseOut)
async def get(id:int):
	return await CoursBaseOut.from_queryset_single(Cours.get(id=id))

@router.post("/", response_model=CoursBaseOut)
async def create(cours:CoursBaseIn):
	new_cours = await Cours.create(**cours.dict(exclude_unset=True))
	return new_cours

@router.put("/{id}", response_model=CoursBaseOut)
async def put(id:int, cours:CoursBaseIn):
	await Cours.filter(id=id).update(**cours.dict(exclude_unset=True))
	return await CoursBaseOut.from_queryset_single(Cours.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await Cours.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Cours {id} not found")
    return {"deleted": id}
