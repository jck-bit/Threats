from django.shortcuts import render
from . models import Post
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    context ={
        'posts':Post.objects.all()
    }
    return render(request, 'posts/home.html', context)


def about(request):
    return render(request, 'posts/about.html')