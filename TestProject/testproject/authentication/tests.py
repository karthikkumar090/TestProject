import pytest
from django.test import TestCase
from pytest_common_subject import precondition_fixture
from pytest_django.fixtures import db
from pytest_drf import (
    Returns200,
    Returns201,
    Returns204,
    UsesDeleteMethod,
    UsesDetailEndpoint,
    UsesGetMethod,
    UsesListEndpoint,
    UsesPatchMethod,
    UsesPostMethod,
    ViewSetTest,
)
from pytest_drf.util import url_for
from pytest_lambda import lambda_fixture, static_fixture
from rest_framework.test import APIClient

from authentication import serializers
from authentication.models import User

client = APIClient()
user_data = {
    "email": "test@test.com",
    "firstName": "test",
    "lastName": "test",
    "password": "T@st1234",
    "confirmPassword": "T@st1234",
    "phoneNumber": "182810018",
}


USER_EMAIL = user_data["email"]

user_fixture = static_fixture(user_data)

verification_code = None


@pytest.mark.django_db
class TestRegister(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for("rest_register"))

    class TestUserCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        data = user_fixture

        def test_it_creates_new_user(self, json):
            expected = {}
            actual = json
            user = User.objects.get(email=USER_EMAIL)
            assert expected == actual

@pytest.mark.django_db
class TestInvalidRegister(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.reg_url = "/user/registration"

    def test_invalid_register(self):
        user_data_copy = user_data.copy()
        user_data_copy["confirmPassword"] = "not matching fake value"
        resp = client.post(self.reg_url, user_data_copy, format="json")
        assert resp.status_code == 400
        assert resp.json()["confirmPassword"] == [
            "Confirm password does not match"
        ]
