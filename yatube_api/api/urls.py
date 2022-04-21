from xml.etree.ElementInclude import include
from django.urls import include, path
from rest_framework import routers

from api.views import PostView, GroupView, CommentView, FollowViews


router = routers.DefaultRouter()

router.register('v1/posts', PostView, basename='post')
router.register('v1/groups',GroupView, basename='group')
router.register('v1/comments', CommentView, basename='comment')
router.register('v1/follows', FollowViews, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
]
