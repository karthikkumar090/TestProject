from django.db import models

from testproject.models import BaseModel
from authentication.models import User


class NewGroup(BaseModel):
    group_created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="group_created_by"
    )
    group_name = models.CharField(max_length=124, null=True, default=None)
    group_description = models.CharField(
        max_length=1024, null=True, default=None
    )

class GroupMember(BaseModel):
    group = models.ForeignKey(
        NewGroup,
        on_delete=models.DO_NOTHING,
        related_name="group_members",
    )
    members = models.ManyToManyField(User, related_name="group_members")


class Chat(BaseModel):
    group_members_group = models.ForeignKey(
        GroupMember, on_delete=models.DO_NOTHING
    )
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    message = models.TextField(null=True, default=None)
    message_date = models.DateTimeField(null=True, default=None)