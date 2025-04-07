from tortoise import fields
from tortoise.models import Model


class PlayerModel(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=255, unique=True)
    x = fields.IntField(default=0)
    y = fields.IntField(default=0)
    hp = fields.IntField(default=100)

    class Meta:
        table = "players"
        