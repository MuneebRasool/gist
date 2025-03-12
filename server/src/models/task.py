from tortoise import fields, models
from uuid import UUID


class Task(models.Model):
    """
    Task model that represents the tasks table in the database.
    """
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='tasks')
    task = fields.CharField(max_length=500)
    message_id = fields.CharField(max_length=255)
    priority = fields.CharField(max_length=50, null=True)
    deadline = fields.CharField(max_length=100, null=True)
    relevance_score = fields.FloatField(null=True)
    utility_score = fields.FloatField(null=True)
    cost_score = fields.FloatField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "tasks"

    def __str__(self):
        return f"{self.task} (User: {self.user_id})"

    class PydanticMeta:
        exclude = ["user"]
