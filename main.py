from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

from tortoise.contrib.fastapi import register_tortoise

from models import *

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

register_tortoise(
	app,
	db_url = 'sqlite://db.sqlite3',
	modules = {'models':['main']},
	generate_schemas = True,
	add_exception_handlers = True
)
