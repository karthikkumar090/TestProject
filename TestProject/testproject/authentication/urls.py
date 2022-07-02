from django.urls import include, path, re_path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import LogoutView
from rest_framework import routers

from authentication import views

rest_auth_router = routers.SimpleRouter(trailing_slash=False)
router = routers.DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("", include(rest_auth_router.urls)),
    path("registration", views.RegisterView.as_view(), name="rest_register"),
    path("login", views.LoginView.as_view(), name="rest_login"),
    path("logout", LogoutView.as_view(), name="rest_logout"),
    path("edit_user/", views.EditProfile.as_view(), name="edit_user"),
    re_path(
        r"^account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
        name='account_confirm_email'),
]
