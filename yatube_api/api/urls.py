from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

v1_router = SimpleRouter()
v1_router.register(r'posts', PostViewSet, basename='posts')
v1_router.register(r'groups', GroupViewSet)
v1_router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                   basename='comments')
v1_router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
