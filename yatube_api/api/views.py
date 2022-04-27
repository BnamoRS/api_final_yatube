from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Follow, Group, Post
from .permissions import IsAuthorObjectPermission
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorObjectPermission, IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorObjectPermission, IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        return serializer.save(author=self.request.user, post=post_id)


class FollowViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.ViewSet):
    queryset=Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthorObjectPermission, IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.validated_data.get('following') == self.request.user:
            raise serializers.ValidationError(
                {"detail": "Подписка на самого себя невозможна"}
            )
        return serializer.save(user=self.request.user)
