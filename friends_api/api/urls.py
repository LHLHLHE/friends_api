from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
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

schema_view = get_schema_view(
    openapi.Info(
        title="FriendsAPI",
        default_version='v1.0',
        description="Документация для FriendsAPI",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('v1/auth/', include('djoser.urls.authtoken')),
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.base')),
    path(
        'v1/redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
