from typing import List, Dict
from fastapi import APIRouter, HTTPException
from models import Class, PydanticClass, PydanticClassIn

router = APIRouter()

@router.get("/", response_model=List[PydanticClass])
async def read():
	return await PydanticClass.from_queryset(Class.all())

@router.get("/{id}", response_model=PydanticClass)
async def get(id:int):
	return await PydanticClass.from_queryset_single(Class.get(id=id))

@router.post("/", response_model=PydanticClass)
async def create(classe:PydanticClassIn):
	new_classe = await Class.create(**classe.dict(exclude_unset=True))
	return await PydanticClass.from_tortoise_orm(new_classe)

@router.put("/{id}", response_model=PydanticClass)
async def put(id:int, classe:PydanticClassIn):
	await Class.filter(id=id).update(**classe.dict(exclude_unset=True))
	return await PydanticClass.from_queryset_single(Class.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await Class.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Class {id} not found")
    return {"deleted": id}
