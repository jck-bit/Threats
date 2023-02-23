from .import views 
from django.urls import path
from .views import  PostDetailView, PostUpdateView,PostDeleteView,PostCreateView

urlpatterns = [
    path('', views.home, name='post-home'),
    path('upload/', PostCreateView.as_view(), name='post-upload'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete')
]