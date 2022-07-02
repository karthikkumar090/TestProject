from rest_framework import serializers

from chat.models import (
    NewGroup,
    Chat,
)


class NewGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewGroup
        fields = "__all__"



class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
