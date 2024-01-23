from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, serializers, status, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Post, Group, Follow
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer)
from .permissions import OwnerOrReadOnly


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (OwnerOrReadOnly,)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        group_id = self.request.data.get('group')
        if self.request.user.is_authenticated:
            author = self.request.user
            group = get_object_or_404(Group, id=group_id) if group_id else None
            serializer.save(author=author, group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'detail': 'Authentication credentials were not provided.'}, 
                status=status.HTTP_401_UNAUTHORIZED)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
