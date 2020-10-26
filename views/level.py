from typing import List, Dict
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator
from models import Level

PydanticLevel = pydantic_model_creator(Level, name='Level')
PydanticLevelIn = pydantic_model_creator(Level, name='LevelIn', exclude_readonly=True)

router = APIRouter()

@router.get("/", response_model=List[PydanticLevel])
async def read():
	return await PydanticLevel.from_queryset(Level.all())

@router.get("/{id}", response_model=PydanticLevel)
async def get(id:int):
	return await PydanticLevel.from_queryset_single(Level.get(id=id))

@router.post("/", response_model=PydanticLevel)
async def create(level:PydanticLevelIn):
	new_level = await Level.create(**level.dict(exclude_unset=True))
	return await PydanticLevel.from_tortoise_orm(new_level)

@router.put("/{id}", response_model=PydanticLevel)
async def put(id:int, level:PydanticLevelIn):
	await Level.filter(id=id).update(**level.dict(exclude_unset=True))
	return await PydanticLevel.from_queryset_single(Level.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await Level.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Level {id} not found")
    return {"deleted": id}
