from xml.etree.ElementInclude import include
from django.urls import include, path
from rest_framework import routers

from api.views import PostView, GroupView, CommentView, FollowViews


router = routers.DefaultRouter()

router.register('posts', PostView, basename='post')
router.register('groups',GroupView, basename='group')
#router.register('follow', FollowViews, basename='follow')
router.register(r'^posts/(?P<post_id>\d+)/comments', CommentView, basename='comment')


urlpatterns = [
    path('v1/', include(router.urls)),
    #path('v1/groups/<int:pk>/', GroupView.as_view(), name='group'),
    #path('v1/groups/', GroupsView.as_view(), name='group'),
    path('v1/follow/', FollowViews.as_view(), name='follow'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
