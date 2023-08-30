from django.contrib import admin
from .models import Post, LikePost,Follow,Comment,Reply

admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Reply)