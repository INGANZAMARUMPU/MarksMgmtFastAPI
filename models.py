from tortoise import Tortoise, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel

class Section(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)

    def __str__(self):
    	return name

class Level(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    level = fields.IntField(null=True)

    def __str__(self):
    	return name

class AnneScolaire(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)

    def __str__(self):
    	return name

class Class(models.Model):
    id = fields.IntField(pk=True)
    level = fields.ForeignKeyField('models.Level', null=False, blank=False)
    section = fields.ForeignKeyField('models.Section', null=False, blank=False)
    a_s = fields.ForeignKeyField('models.AnneScolaire', null=False, blank=False)

    def level_name(self) -> str:
    	return "{self.level.name}"

    def section_name(self) -> str:
    	return "{self.section.name}"

    def a_s_name(self) -> str:
    	return "{self.a_s.name}"

    def __str__(self) -> str:
        return "{self.level.name} {self.section.name}"

    class PydanticMeta:
        computed = ["level_name", "section_name", "a_s_name"]

class Student(models.Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    classe = fields.ForeignKeyField('models.Class', null=False, blank=False)

    def fullName(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def classe_name(self) -> str:
    	return "{self.classe.name}"

    class PydanticMeta:
        computed = ["fullName", "classe_name"]

class Cours(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)
    hours = fields.IntField(null=True)
    classe = fields.ForeignKeyField('models.Class', null=False)
    teacher = fields.ForeignKeyField('models.User', null=False)

class Work(models.Model):
    cours = fields.ForeignKeyField('models.Cours', null=False)
    date = fields.DatetimeField(auto_now_add=True)

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    category = fields.CharField(max_length=30, default="misc")
    password_hash = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class PydanticMeta:
        computed = ["full_name"]
        exclude = ["password_hash"]

PydanticUser = pydantic_model_creator(User, name='User')
PydanticUserIn = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)