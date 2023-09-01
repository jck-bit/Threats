from .import views 
from django.urls import path
from .views import  PostDetailView, PostUpdateView,PostDeleteView,PostCreateView

urlpatterns = [
    path('', views.home, name='post-home'),
    path('upload/', PostCreateView.as_view(), name='post-upload'),
    path('like-post/', views.like_post, name='like-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/comment/<int:comment_id>/', views.get_detailview_of_comment, name='comment-detail'),
    path('post/<int:post_id>/comment/', views.create_comment, name='create-comment'),
    path('post/<int:post_id>/comment/<int:comment_id>/reply/', views.create_reply, name='create-reply'),
    path('post/<int:post_id>/comment/<int:comment_id>/reply/<int:reply_id>/', views.get_detailview_of_reply, name='reply-detail'),
    path('post/<int:post_id>/comment/<int:comment_id>/reply/<int:parent_reply_id>/reply/', views.create_reply_to_another_reply, name='create-reply-to-reply'),
]