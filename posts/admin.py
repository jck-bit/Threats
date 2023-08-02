from django.contrib import admin
from .models import Post, LikePost,Follow

admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Follow)