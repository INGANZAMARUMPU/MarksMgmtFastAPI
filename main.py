from typing import Optional
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware

from views import *

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(section.router, prefix="/section")
app.include_router(level.router, prefix="/level")
app.include_router(classe.router, prefix="/classe")
app.include_router(annee_scolaire.router, prefix="/annee_scolaire")
app.include_router(student.router, prefix="/student")
app.include_router(cours.router, prefix="/cours")
app.include_router(work.router, prefix="/work")
app.include_router(user.router, prefix="/user")
app.include_router(authentication.router, prefix="/authentication")

register_tortoise(
	app,
	db_url = 'sqlite://db.sqlite3',
	modules = {'models':['models']},
	generate_schemas = True,
	add_exception_handlers = True
)
