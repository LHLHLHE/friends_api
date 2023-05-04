from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    UserViewSet,
    FriendshipRequestCreateDestroyViewSet,
    FriendshipRequestViewSet,
    FriendViewSet
)

router_v1 = DefaultRouter()

router_v1.register('users/friends', FriendViewSet, basename='friends')
router_v1.register(
    r'users/(?P<user_id>\d+)/friend',
    FriendshipRequestCreateDestroyViewSet,
    basename='send_delete_friendship-request'
)
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    'friendship-requests',
    FriendshipRequestViewSet,
    basename='friendship_requests'
)

urlpatterns = [
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.base')),
]
