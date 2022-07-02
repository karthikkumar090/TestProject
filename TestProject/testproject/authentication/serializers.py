
from allauth.account import app_settings as allauth_settings
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer
from rest_framework import exceptions, serializers
from rest_framework.serializers import ValidationError

from .fields import IMCharField, IMEmailField

IMS = settings.IDENTITY_MESSAGE_SETTINGS
IMPasswordRegexValidator = RegexValidator(
    regex=IMS["PASSWORD"]["regex"], message=IMS["PASSWORD"]["regex-message"]
)
User = get_user_model()

admin = "admin"
normal = "normal"

USER_TYPE = (
    ("admin", "admin"),
    ("normal", "normal"),
)


class RegisterSerializer(RegisterSerializer):
    username = password1 = password2 = None
    email = IMEmailField(
        required=allauth_settings.EMAIL_REQUIRED,
        blank_message=IMS["EMAIL"]["blank"],
    )
    first_name = IMCharField(blank_message=IMS["FIRST_NAME"]["blank"])
    last_name = IMCharField(IMS["LAST_NAME"]["blank"])
    password = IMCharField(
        write_only=True,
        blank_message=IMS["PASSWORD"]["blank"],
        validators=[IMPasswordRegexValidator],
    )
    confirm_password = IMCharField()
    user_type = serializers.ChoiceField(choices=USER_TYPE)
    phone_number = IMCharField()

    def validate_first_name(self, fname):
        if not fname.isalpha():
            raise ValidationError(IMS["FIRST_NAME"]["alpha"])
        return fname.capitalize()

    def validate_last_name(self, lname):
        if not lname.isalpha():
            raise ValidationError(IMS["LAST_NAME"]["alpha"])
        return lname.capitalize()

    def validate_confirm_password(self, con_pwd):
        pwd = self.context["request"].data["password"]
        if pwd != con_pwd:
            raise ValidationError(IMS["CONFIRM_PASSWORD"]["mismatch"])

    def validate(self, data):
        phone_number = self.context["request"].data["phone_number"]
        if not self.context["request"].user.is_anonymous:
            raise serializers.ValidationError(IMS["USER"]["logged-in"])
        if (
            phone_number
            and User.objects.filter(
                phone_number=self.context["request"].data["phone_number"]
            ).exists()
        ):
            raise serializers.ValidationError(IMS["PHONE_NUMBER"]["existed"])
        return data

    def get_cleaned_data(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "user_type": self.validated_data.get("user_type", ""),
            "password1": self.validated_data.get("password", ""),
            "password2": self.validated_data.get("password", ""),
            "email": self.validated_data.get("email", "").strip(),
            "username": self.validated_data.get("email", "").strip(),
            "phone_number": self.validated_data.get("phone_number", "").strip(),
        }

    def custom_signup(self, request, user):
        user.phone_number = request.data.get("phone_number")
        user.user_type = request.data.get("user_type")
        user.save()


class LoginSerializer(LoginSerializer):
    username = None
    email = IMCharField(
        blank_message=IMS["EMAIL"]["blank"], required=False, allow_blank=True
    )
    password = IMCharField(
        blank_message=IMS["PASSWORD"]["blank"],
        style={"input_type": "password"},
    )
    user_type = serializers.ChoiceField(choices=USER_TYPE)

    def validate_user_type(self, user_type):
        if user := User.objects.filter(email__iexact=self.context["request"].data["email"]).first():
            user_type_db = user.user_type.strip()
            if self.context["request"].data["user_type"] != user_type_db:
                raise serializers.ValidationError(
                    IMS["USER"]["not-match-type-when-login"]
                )
        return user_type

    def validate_email(self, em):
        em = em.strip()
        if not em:
            raise ValidationError(IMS["EMAIL"]["blank"])
        return em

    def validate_password(self, pwd):
        pwd = pwd.strip()
        if not pwd:
            raise ValidationError(IMS["EMAIL"]["blank"])
        return pwd

    def _validate_email(self, email, password):
        user = None
        user = User.objects.filter(email__iexact=email).first()

        if not user:
            raise ValidationError("Unable to log in with provided credentials")

        if email and password:
            user = self.authenticate(username=user.email, password=password)
        else:
            msg = _(IMS["EMAIL"]["email_pass"])
            raise exceptions.ValidationError(msg)
        return user
