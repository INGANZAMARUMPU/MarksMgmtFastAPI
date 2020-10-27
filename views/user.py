from typing import List, Dict
from fastapi import APIRouter, HTTPException
from tortoise.contrib.pydantic import pydantic_model_creator

from models import User
from .authentication import get_password_hash

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
	dict_user = user.dict(exclude_unset=True)
	password = get_password_hash(user.password)
	dict_user["password_hash"] = password
	new_user = await User.create(**dict_user)
	return await PydanticUser.from_tortoise_orm(new_user)

@router.put("/{id}", response_model=PydanticUser)
async def put(id:int, user:UserIn):
	dict_user = user.dict(exclude_unset=True)
	if(user.password):
		password = get_password_hash(user.password)
		dict_user["password_hash"] = password
	await User.filter(id=id).update(**dict_user)
	return await PydanticUser.from_queryset_single(User.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await User.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return {"deleted": id}
