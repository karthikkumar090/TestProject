from datetime import date

from django.db import transaction
from django.db.models import Q
from django.db.models.functions import Lower
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from .models import NewGroup, Chat, GroupMember
from .serializers import NewGroupSerializer, ChatSerializer

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

# Create your views here.

class NewGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = NewGroupSerializer
    queryset = NewGroup.objects.all()

    def group_create_or_update(self, data):
        with transaction.atomic():
            group_created_by = self.request.user.id
            group_name = data.get("group_name", None)
            group_description = data.get("group_description", None)
            group_id = data.get("group_id", None)

            if not group_id:
                user = User.objects.get(id=group_created_by)
                group = NewGroup.objects.create(
                    group_created_by=user,
                    group_name=group_name,
                    group_description=group_description,
                )
                gm = GroupMember.objects.create(group=group)
                gm.save()
                gm.members.set([self.request.user])
            else:
                group = NewGroup.objects.get(id=group_id)
                group.group_name = group_name
                group.group_description = group_description

        return group

    def list(self, request, *args, **kwargs):
        """
        API end point returns the list of Created Groups of a user when "user_id"
        parameter is passed in query string
        """
        try:
            queryset = self.get_queryset()
            sort_by = request.query_params.get("sort_by", None)
            group_name = request.query_params.get("group_name", None)
            user = self.request.user

            queryset = (
                queryset.filter(
                    Q(group_created_by=user)
                    | Q(group_members__members__id__in=[user.id])
                )
                .distinct()
                .order_by("updated_datetime")
            )

            # Search by group name
            if group_name:
                queryset = queryset.annotate(
                    lower_name=Lower("group_name"),
                    lower_description=Lower("group_description"),
                )
                queryset = queryset.filter(
                    Q(lower_name__contains=group_name.lower())
                    | Q(lower_description__contains=group_name.lower())
                )

            # sort by a-z or z-a
            sort_by_name = {"asc": "group_name", "desc": "-group_name"}
            if sort_by:
                queryset = queryset.order_by(sort_by_name[sort_by.lower()])

            # serialize data
            serializer = self.get_serializer(queryset, many=True).data

            return Response(
                data={
                    "message": "Successfully displaying Group details",
                    "details": serializer,
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as exp_main:
            return Response(
                {"message": str(exp_main)}, status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        """
        This request method is used to create and edit a New Group
        """
        try:
            group_details = request.data
            _group = self.group_create_or_update(group_details)
            serialized_group = NewGroupSerializer(_group)
            return Response(
                data={
                    "message": "New Group created successfully",
                    "details": serialized_group.data,
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as exp:
            import traceback
            traceback.print_exc()
            return Response(
                data={"message": str(exp)}, status=status.HTTP_400_BAD_REQUEST
            )


class ChatViewSet(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ChatSerializer

    def post(self, request):
        try:
            with transaction.atomic():
                sender = request.data.get("sender", None)
                message = request.data.get("message", None)
                group_id = request.data.get("group_id", None)
                if sender and group_id:
                    sender = User.objects.get(id=sender)
                    group = NewGroup.objects.get(id=group_id)
                    group_members_group = GroupMember.objects.get(group=group_id)

                if not sender or not group:
                    raise Exception(
                        "User and Group is required to send a message"
                    )

                if message:
                    chat = Chat.objects.create(
                        sender=sender,
                        message=message,
                        group_members_group=group_members_group,
                        message_date=timezone.now(),
                    )
                    serializer = self.serializer_class(chat)

                    return Response(
                        data={
                            "message": "Chats updated successfully",
                            "details": serializer.data,
                            "success": True,
                        },
                        status=status.HTTP_200_OK,
                    )
        except Exception as exp:
            return Response(
                data={"message": str(exp)}, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request):
        try:
            if group_id := request.GET.get("group_id", None):
                queryset = Chat.objects.filter(
                    group_members_group__group__id=group_id
                ).order_by("-id")
                serializer = self.serializer_class(queryset, many=True)

                return Response(
                    data={
                        "message": "Chats displayed successfully",
                        "details": serializer.data,
                        "success": True,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                raise Exception("Invalid Group Id")

        except Exception as exp:
            return Response(
                data={"message": str(exp)}, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(http_method_names=["POST"])
@authentication_classes([])
@permission_classes([])
def adduser(request):
    try:
        data=request.data
        group_id=data.get("group_id", None)
        user_id=data.get("user_id", None)
        group = NewGroup.objects.get(id=group_id)
        user = User.objects.get(id=user_id)
        group_members = group.group_members.get(group=group)
        
        group_members.members.add(user)

        return Response(
            data={
                "message": "Successfully added member to the Chat Group",
                "success": True,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as exp:
        import traceback
        traceback.print_exc()
        return Response({"message": str(exp)}, status=status.HTTP_400_BAD_REQUEST)