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
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, id=post_id)
        return get_object_or_404(Comment, post=post, id=comment_id)

    def create(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(self.request, post)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(
                serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, post_id, pk, **kwargs):
        partial = kwargs.pop('partial', False)
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, post=post, id=pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(
            comment, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, post_id, pk):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, post=post, id=pk)
        #self.check_object_permissions(request, comment)
        comment.delete()
        
        return Response(
            status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    #queryset=Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        
        print(user.follower.all())
        return user.follower.all()

    def perform_create(self, serializer):
        
        return serializer.save(user=self.request.user)
