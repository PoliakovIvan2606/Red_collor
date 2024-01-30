from django.contrib import admin
from . import models
from django.contrib.auth.models import User

class PostsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text')


admin.site.register(models.Posts, PostsAdmin)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'post', 'user')
    list_display_links = ('id', 'text')
    search_fields = ['text']

admin.site.register(models.Comments, CommentsAdmin)