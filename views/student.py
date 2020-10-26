from typing import List, Dict
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator
from models import Student

PydanticStudent = pydantic_model_creator(Student, name='Student')
PydanticStudentIn = pydantic_model_creator(Student, name='StudentIn', exclude_readonly=True)

class StudentBaseIn(PydanticStudentIn):
    classe_id: int

    class Config:
        orm_mode = True

class StudentBaseOut(PydanticStudent):
    classe_id: int

    class Config:
        orm_mode = True

router = APIRouter()

@router.get("/", response_model=List[StudentBaseOut])
async def read():
	return await StudentBaseOut.from_queryset(Student.all())

@router.get("/{id}", response_model=StudentBaseOut)
async def get(id:int):
	return await StudentBaseOut.from_queryset_single(Student.get(id=id))

@router.post("/", response_model=StudentBaseOut)
async def create(student:StudentBaseIn):
	new_student = await Student.create(**student.dict(exclude_unset=True))
	return new_student

@router.put("/{id}", response_model=StudentBaseOut)
async def put(id:int, student:StudentBaseIn):
	await Student.filter(id=id).update(**student.dict(exclude_unset=True))
	return await StudentBaseOut.from_queryset_single(Student.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await Student.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    return {"deleted": id}
