from .import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='post-home'),
    path('about/', views.about, name='post-about')
]