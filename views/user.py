from typing import List, Dict
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator

from models import User

PydanticUser = pydantic_model_creator(User, name='User')
PydanticUserIn = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

class UserIn(PydanticUserIn):
	password:str

router = APIRouter()

@router.get("/", response_model=List[PydanticUser])
async def read():
	return await PydanticUser.from_queryset(User.all())

@router.get("/{id}", response_model=PydanticUser)
async def get(id:int):
	return await PydanticUser.from_queryset_single(User.get(id=id))

@router.post("/", response_model=PydanticUser)
async def create(user:UserIn):
	new_user = await User.create(**user.dict(exclude_unset=True))
	return await PydanticUser.from_tortoise_orm(new_user)

@router.put("/{id}", response_model=PydanticUser)
async def put(id:int, user:UserIn):
	await User.filter(id=id).update(**user.dict(exclude_unset=True))
	return await PydanticUser.from_queryset_single(User.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await User.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return {"deleted": id}
