from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from posts.models import Comment, Follow, Group, Post, User
from .permissions import IsAuthorObjectPermission
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorObjectPermission)
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

    def get_object(self):
        queryset = self.get_queryset()
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('pk')
        print(post_id)
        print(comment_id)
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(queryset, post=post, id=comment_id)
        self.check_object_permissions(self.request, comment)
        return comment

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)
        return serializer

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
        return serializer

    def perform_destroy(self, instance):
        instance.delete()


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return user.follower.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
