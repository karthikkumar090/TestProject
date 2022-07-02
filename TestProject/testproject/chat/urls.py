from django.urls import include, path
from rest_framework import routers

from chat import views

test_router = routers.SimpleRouter(trailing_slash=False)
router = routers.DefaultRouter()

router.register("newgroup", views.NewGroupViewSet)

urlpatterns = [
    path("", include(test_router.urls)),
    path("", include(router.urls)),
    path("chat/", views.ChatViewSet.as_view()),
    path("adduser/", views.adduser, name="adduser"),
]
