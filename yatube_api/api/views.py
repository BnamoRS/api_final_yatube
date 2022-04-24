from django.shortcuts import get_object_or_404
from requests import request
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from api.permissions import IsAuthorPermission
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
from posts.models import Post, Group, Comment, Follow, User


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorPermission,)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


#class GroupsView(generics.ListAPIView):
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer


class GroupView(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentView(viewsets.ModelViewSet):
    #queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorPermission,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class FollowViews(generics.ListCreateAPIView):
    serializer_class = FollowSerializer

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return user.follower.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
