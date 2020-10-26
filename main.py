from typing import Optional
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from views import section, level, annee_scolaire, classe

app = FastAPI()

app.include_router(section.router, prefix="/section")
app.include_router(level.router, prefix="/level")
app.include_router(classe.router, prefix="/classe")
app.include_router(annee_scolaire.router, prefix="/annee_scolaire")

register_tortoise(
	app,
	db_url = 'sqlite://db.sqlite3',
	modules = {'models':['models']},
	generate_schemas = True,
	add_exception_handlers = True
)
