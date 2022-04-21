from rest_framework import viewsets

from api.serializers import PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
from posts.models import Post, Group, Comment, Follow


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class GroupView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class FollowViews(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
