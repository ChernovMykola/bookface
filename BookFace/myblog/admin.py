from django.contrib import admin

from myblog.models import Comment, Post, UserProfileInfo

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfileInfo)
