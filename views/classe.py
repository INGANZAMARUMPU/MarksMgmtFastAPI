from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi.security import OAuth2PasswordBearer

from models import Class, User
from .authentication import get_current_user

PydanticClass = pydantic_model_creator(Class, name='Class')
PydanticClassIn = pydantic_model_creator(Class, name='ClassIn', exclude_readonly=True)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication/token")

class ClassBaseIn(PydanticClassIn):
    level_id: int
    section_id: int
    a_s_id: int

    class Config:
        orm_mode = True

class ClassBaseOut(PydanticClass):
    level_id: int
    section_id: int
    a_s_id: int

    class Config:
        orm_mode = True

@router.get("/", response_model=List[ClassBaseOut])
async def read(current_user: User = Depends(get_current_user)):
    classes = Class.all().select_related("level","section","a_s")
    return await ClassBaseOut.from_queryset(classes)

@router.get("/{id}", response_model=ClassBaseOut)
async def get(id:int):
	return await ClassBaseOut.from_queryset_single(Class.get(id=id))

@router.post("/", response_model=ClassBaseOut)
async def create(classe:ClassBaseIn):
	new_classe = await Class.create(**classe.dict(exclude_unset=True))
	return new_classe

@router.put("/{id}", response_model=ClassBaseOut)
async def put(id:int, classe:ClassBaseIn):
	await Class.filter(id=id).update(**classe.dict(exclude_unset=True))
	return await ClassBaseOut.from_queryset_single(Class.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await Class.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Class {id} not found")
    return {"deleted": id}
