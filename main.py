from typing import Optional
from fastapi import FastAPI

from tortoise.contrib.fastapi import register_tortoise

from views import section

app = FastAPI()

app.include_router(
    section.router,
    prefix="/section",
)

register_tortoise(
	app,
	db_url = 'sqlite://db.sqlite3',
	modules = {'models':['models']},
	generate_schemas = True,
	add_exception_handlers = True
)
