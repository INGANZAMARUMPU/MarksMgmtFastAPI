from tortoise import Tortoise, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

Tortoise.init_models(["main"], "models")

class Section(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)

    def __str__(self):
    	return name

PydanticSection = pydantic_model_creator(Section, name='Section')
PydanticSectionIn = pydantic_model_creator(Section, name='SectionIn', exclude_readonly=True)

class Level(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)
    level = fields.IntField(null=True)

    def __str__(self):
    	return name

PydanticLevel = pydantic_model_creator(Level, name='Level')
PydanticLevelIn = pydantic_model_creator(Level, name='LevelIn', exclude_readonly=True)

class AnneScolaire(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50, null=True)

    def __str__(self):
    	return name

PydanticAS = pydantic_model_creator(AnneScolaire, name='AnneScolaire')
PydanticASIn = pydantic_model_creator(AnneScolaire, name='AnneScolaireIn', exclude_readonly=True)

class Class(models.Model):
    id = fields.IntField(pk=True)
    level:fields.ForeignKeyRelation[Level] = \
    	fields.ForeignKeyField('models.Level', null=False, blank=False)
    section:fields.ForeignKeyRelation[Section] = \
    	fields.ForeignKeyField('models.Section', null=False, blank=False)
    a_s:fields.ForeignKeyRelation[Section] = \
    	fields.ForeignKeyField('models.AnneScolaire', null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.level.name} {self.section.name}"

PydanticClass = pydantic_model_creator(Class, name='Class')
PydanticClassIn = pydantic_model_creator(Class, name='ClassIn', exclude_readonly=True)

class Student(models.Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    classe = fields.ForeignKeyField('models.Class', null=False, blank=False)

    def fullName(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class PydanticMeta:
        computed = ["fullName"]

PydanticStudent = pydantic_model_creator(Student, name='Student')
PydanticStudentIn = pydantic_model_creator(Student, name='StudentIn', exclude_readonly=True)

class Cours(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)
    hours = fields.IntField(null=True)
    classe = fields.ForeignKeyField('models.Class', null=False)
    teacher = fields.ForeignKeyField('models.User', null=False)

PydanticCours = pydantic_model_creator(Cours, name='Cours')
PydanticCoursIn = pydantic_model_creator(Cours, name='CoursIn', exclude_readonly=True)

class Work(models.Model):
    cours = fields.ForeignKeyField('models.Cours', null=False)
    date = fields.DatetimeField(auto_now_add=True)

PydanticWork = pydantic_model_creator(Work, name='Work')
PydanticWorkIn = pydantic_model_creator(Work, name='WorkIn', exclude_readonly=True)

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