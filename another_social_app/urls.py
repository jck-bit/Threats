"""another_social_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from posts.views import  PostDetailView, PostUpdateView,PostDeleteView,PostCreateView
from posts import views as post_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('profile-edit/', user_views.profile_edit, name='profile-edit'),
    path('profile/<int:pk>/', user_views.ProfileView.as_view(template_name='users/profile'), name='profile-view'),
    path('suggested-users/', user_views.suggested_users, name='suggested_users'),
    path('follow-user/<int:pk>/', user_views.follow_user, name='follow-user'),
    
    
    path('', post_views.home, name='post-home'),
    path('upload/', PostCreateView.as_view(), name='post-upload'),
    path('like-post/', post_views.like_post, name='like-post'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/comment/<int:comment_id>/', post_views.get_detailview_of_comment, name='comment-detail'),
    path('post/<int:post_id>/comment/', post_views.create_comment, name='create-comment'),
    path('post/<int:post_id>/comment/<int:comment_id>/reply/', post_views.create_reply, name='create-reply'),
    path('post/<int:post_id>/comment/<int:comment_id>/reply/<int:reply_id>/', post_views.get_detailview_of_reply, name='reply-detail'),
    path('post/<int:post_id>/comment/<int:comment_id>/reply/<int:parent_reply_id>/reply/', post_views.create_reply_to_another_reply, name='create-reply-to-reply'),


    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
