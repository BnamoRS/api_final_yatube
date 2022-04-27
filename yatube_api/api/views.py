from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from posts.models import Comment, Follow, Group, Post
from .permissions import IsAuthorObjectPermission
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #permission_classes = (IsAuthorObjectPermission, IsAuthenticatedOrReadOnly,)
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

    def create(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.validated_data)
        return Response(serializer.errors)

    def update(self, request, post_id, pk, **kwargs):
        partial = kwargs.pop('partial', False)
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=pk)
        serializer = CommentSerializer(
            comment, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data)
        return Response(serializer.errors)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    #queryset=Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthorObjectPermission, IsAuthenticatedOrReadOnly,)
    #filter_backends = (filters.SearchFilter,)
    #search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        print(user.follower.all())
        return user.follower.all()

    def perform_create(self, serializer):
        
        return serializer.save(user=self.request.user)
