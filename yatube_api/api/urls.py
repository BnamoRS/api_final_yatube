from xml.etree.ElementInclude import include
from django.urls import include, path
from rest_framework import routers

from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowView





router = routers.DefaultRouter()

router.register('posts', PostViewSet, basename='post')
router.register('groups',GroupViewSet, basename='group')
router.register(
    r'^posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('v1/follow/', FollowView.as_view(), name='follow'),
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
