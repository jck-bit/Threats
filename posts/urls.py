from .import views 
from django.urls import path
from .views import PostCreateView, PostDetailView, PostUpdateView


urlpatterns = [
    path('', views.home, name='post-home'),
    path('about/', views.about, name='post-about'),
    path('upload/', views.upload, name='post-upload'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update')
]