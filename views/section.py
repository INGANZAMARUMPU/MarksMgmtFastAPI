from typing import List
from fastapi import APIRouter
from models import Section, PydanticSection, PydanticSectionIn

router = APIRouter()

@router.get("/")
async def read():
	return await PydanticSection.from_queryset(Section.all())

@router.get("/{id}")
async def get(id:int)->PydanticSection:
	return await PydanticSection.from_queryset_single(Section.get(id=id))

@router.post("/")
async def create(section:PydanticSectionIn)->PydanticSection:
	new_section = await Section.create(**section.dict(exclude_unset=True))
	return await PydanticSection.from_tortoise_orm(new_section)

@router.put("/{id}")
async def put(id:int, section:PydanticSectionIn)->PydanticSection:
	await Section.filter(id=id).update(**section.dict(exclude_unset=True))
	return await PydanticSection.from_queryset_single(Section.get(id=id))

@router.delete("/{id}")
async def delete(id:int):
    deleted = await Section.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Section {id} not found")
    return {"deleted": id}

# @router.put("/{id}")
# async def put(id:int, section:PydanticSectionIn)->PydanticSection:
# 	old = await Section.get(id=id)
# 	new = await old.update_from_dict(section.dict(exclude_unset=True))
# 	return new
