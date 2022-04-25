from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from requests import request
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorPermission
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
from posts.models import Post, Group, Comment, Follow, User


class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorPermission,)
    pagination_class = LimitOffsetPagination

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
    #queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,) # DjangoFilterBackend)
    # filterset_fields = ('following',)
    search_fields = ('user__username',)

    def get_queryset(self):
        following = self.request.user.id
        print(self.request.user.id)
        print(Follow.objects.filter(following=following))
        
        return Follow.objects.filter(following=following)

    def perform_create(self, serializer):
        print(serializer.instance)
        print(serializer.validated_data.get('following').id)
        print(self.request.user.id)
        return serializer.save(user=self.request.user)
