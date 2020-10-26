from typing import List, Dict
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator
from models import AnneScolaire as AS

PydanticAS = pydantic_model_creator(AS, name='AnneScolaire')
PydanticASIn = pydantic_model_creator(AS, name='AnneScolaireIn', exclude_readonly=True)

router = APIRouter()

@router.get("/", response_model=List[PydanticAS])
async def read():
	return await PydanticAS.from_queryset(AS.all())

@router.get("/{id}", response_model=PydanticAS)
async def get(id:int):
	return await PydanticAS.from_queryset_single(AS.get(id=id))

@router.post("/", response_model=PydanticAS)
async def create(a_s:PydanticASIn):
	new_a_s = await AS.create(**a_s.dict(exclude_unset=True))
	return await PydanticAS.from_tortoise_orm(new_a_s)

@router.put("/{id}", response_model=PydanticAS)
async def put(id:int, a_s:PydanticASIn):
	await AS.filter(id=id).update(**a_s.dict(exclude_unset=True))
	return await PydanticAS.from_queryset_single(AS.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await AS.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"AS {id} not found")
    return {"deleted": id}
