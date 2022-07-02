import io

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from chat.models import NewGroup

class ChatTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create()
        NewGroup.objects.create(group_name="g1", group_description="d1")

    def test_chat_creation(self):
        user = get_user_model().objects.first()
        group = NewGroup.objects.first()
        data = {"sender": user.id ,"message": "how are you", "group_id":group.id}
        response = self.client.post("/chat/chat/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @classmethod
    def tearDownClass(cls):
        get_user_model().objects.all().delete()
        NewGroup.objects.all().delete()