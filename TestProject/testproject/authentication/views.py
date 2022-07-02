from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.db import transaction
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

IMS = settings.IDENTITY_MESSAGE_SETTINGS

User = get_user_model()

def im_do_login(request, user):
    login(request, user, backend=IMS["backend"])
    user_data = {
        "id": user.pk,
        "key": Token.objects.get(user=user).key,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone_number": user.phone_number,
        "user_type": user.user_type,
    }
    return Response(
        data={
            "message": "Succesfully registered and logged in",
            "details": user_data,
            "success": True,
        },
        status=status.HTTP_200_OK,
    )

class RegisterView(RegisterView):
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        return im_do_login(request, user)

class LoginView(LoginView):
    authentication_classes = []

    def get_response(self):
        serializer_class = self.get_response_serializer()
        serializer = serializer_class(
            instance=self.token, context={"request": self.request}
        )
        serialier_data = serializer.data
        serialier_data["id"] = self.user.pk
        serialier_data["first_name"] = self.user.first_name
        serialier_data["last_name"] = self.user.last_name
        serialier_data["email"] = self.user.email
        serialier_data["phone_number"] = self.user.phone_number  
        serialier_data["user_type"] = self.user.user_type

        return Response(
            data={
                "message": "Succesfully logged in",
                "details": serialier_data,
                "success": True,
            },
            status=status.HTTP_200_OK,
        )


class EditProfile(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        try:
            with transaction.atomic():
                user_obj = User.objects.get(id=request.data.get("id"))
                new_first_name = request.data.get("first_name", None)
                new_last_name = request.data.get("last_name", None)
                new_phone_number = request.data.get("phone_number", None)

                if new_first_name:
                    user_obj.first_name = new_first_name
                if new_last_name:
                    user_obj.last_name = new_last_name

                if new_phone_number:
                    if (
                        User.objects.filter(phone_number=new_phone_number).exists()
                        and user_obj.phone_number != new_phone_number
                    ):
                        raise Exception(
                            "A user has already been registered with this phone number"
                        )
                    user_obj.phone_number = new_phone_number
                user_obj.save()

                user_data = {
                    "id": user_obj.pk,
                    "first_name": user_obj.first_name,
                    "last_name": user_obj.last_name,
                    "email": user_obj.email,
                    "phone_number": user_obj.phone_number,
                    "user_type": user_obj.user_type,
                }

            return Response(
                data={
                    "message": "Successfully updated profile",
                    "details": user_data,
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as exp:
            return Response({"message": str(exp)}, status=status.HTTP_400_BAD_REQUEST)


