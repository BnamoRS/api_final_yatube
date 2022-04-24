from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from api.views import FollowViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/follow/', FollowViews.as_view(), name='follow'),
    path('api/', include('api.urls')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
