from djoser.views import UserViewSet
from rest_framework import viewsets, status, mixins, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import (
    UserSerializer,
    UserMeSerializer,
    FriendshipRequestSerializer
)
from users.models import User, FriendshipRequest


class UserViewSet(UserViewSet):
    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'me':
            return UserMeSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()


class FriendshipRequestBaseViewSet(viewsets.GenericViewSet):
    serializer_class = FriendshipRequestSerializer


class FriendshipRequestViewSet(
    mixins.ListModelMixin,
    FriendshipRequestBaseViewSet
):
    def get_queryset(self):
        request = self.request

        if (
            'from-me' in request.query_params
            and request.query_params['from-me']
        ):
            return request.user.from_me_requests.all()

        return request.user.to_me_requests.exclude(status='rejected')

    @action(methods=['post'], detail=True, url_path='accept')
    def accept_request(self, request, pk):
        friend_request = FriendshipRequest.objects.get(id=pk)

        if friend_request.to_user == request.user:
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path='reject')
    def reject_request(self, request, pk):
        friend_request = FriendshipRequest.objects.get(id=pk)

        if friend_request.to_user == request.user:
            friend_request.status = 'rejected'
            friend_request.save(update_fields=['status'])
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class FriendshipRequestCreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    FriendshipRequestBaseViewSet
):
    queryset = FriendshipRequest.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['friend_id'] = self.kwargs.get('user_id')

        return context

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')

        to_friend_request = FriendshipRequest.objects.filter(
            from_user_id=user_id,
            to_user=request.user
        )

        if to_friend_request.exists():
            to_user = get_object_or_404(User, id=user_id)
            request.user.friends.add(to_user)
            to_user.friends.add(request.user)
            to_friend_request.delete()
            return Response(
                {'status': 'Пользователь добавлен в друзья'},
                status=status.HTTP_200_OK
            )

        return super().create(request)

    def perform_create(self, serializer):
        request_user = self.request.user

        serializer.save(
            from_user=request_user,
            to_user=get_object_or_404(
                User,
                id=self.kwargs.get('user_id')
            )
        )

    @action(methods=['delete'], detail=True)
    def delete(self, request, user_id):
        get_object_or_404(
            FriendshipRequest,
            from_user=request.user,
            to_user=user_id
        ).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.friends.all()

    @action(methods=['delete'], detail=True)
    def delete_friend(self, request, pk):
        friend_to_delete = get_object_or_404(User, id=pk)
        request.user.friends.remove(friend_to_delete)
        friend_to_delete.friends.remove(request.user)

        return Response(status=status.HTTP_204_NO_CONTENT)
