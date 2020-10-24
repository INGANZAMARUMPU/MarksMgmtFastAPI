from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class User(models.Model):
    """
    The User model
    """
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