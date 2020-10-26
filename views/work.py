from typing import List, Dict
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator
from models import Work

PydanticWork = pydantic_model_creator(Work, name='Work')
PydanticWorkIn = pydantic_model_creator(Work, name='WorkIn', exclude_readonly=True)

class WorkBaseIn(PydanticWorkIn):
    cours_id: int

    class Config:
        orm_mode = True

class WorkBaseOut(PydanticWork):
    cours_id: int

    class Config:
        orm_mode = True

router = APIRouter()

@router.get("/", response_model=List[WorkBaseOut])
async def read():
	return await WorkBaseOut.from_queryset(Work.all())

@router.get("/{id}", response_model=WorkBaseOut)
async def get(id:int):
	return await WorkBaseOut.from_queryset_single(Work.get(id=id))

@router.post("/", response_model=WorkBaseOut)
async def create(work:WorkBaseIn):
	new_work = await Work.create(**work.dict(exclude_unset=True))
	return new_work

@router.put("/{id}", response_model=WorkBaseOut)
async def put(id:int, work:WorkBaseIn):
	await Work.filter(id=id).update(**work.dict(exclude_unset=True))
	return await WorkBaseOut.from_queryset_single(Work.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await Work.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Work {id} not found")
    return {"deleted": id}
