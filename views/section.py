from typing import List, Dict
from fastapi import APIRouter, HTTPException
from models import Section, PydanticSection, PydanticSectionIn

router = APIRouter()

@router.get("/", response_model=List[PydanticSection])
async def read():
	return await PydanticSection.from_queryset(Section.all())

@router.get("/{id}", response_model=PydanticSection)
async def get(id:int):
	return await PydanticSection.from_queryset_single(Section.get(id=id))

@router.post("/", response_model=PydanticSection)
async def create(section:PydanticSectionIn):
	new_section = await Section.create(**section.dict(exclude_unset=True))
	return await PydanticSection.from_tortoise_orm(new_section)

@router.put("/{id}", response_model=PydanticSection)
async def put(id:int, section:PydanticSectionIn):
	await Section.filter(id=id).update(**section.dict(exclude_unset=True))
	return await PydanticSection.from_queryset_single(Section.get(id=id))

@router.delete("/{id}", response_model=dict)
async def delete(id:int):
    deleted = await Section.filter(id=id).delete()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Section {id} not found")
    return {"deleted": id}
