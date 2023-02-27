from django.contrib import admin
from .models import Post, LikePost

admin.site.register(Post)
admin.site.register(LikePost)