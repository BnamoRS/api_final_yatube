from django.contrib import admin
from posts.models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "following")
    search_fields = ("user", "following")

admin.site.register(Follow, FollowAdmin)
