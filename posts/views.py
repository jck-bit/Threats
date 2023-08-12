from django.shortcuts import render, redirect
from . models import Post,LikePost
from django.contrib.auth.decorators import login_required
from django.views.generic import  CreateView, DetailView, UpdateView, DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse

@login_required
def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    
    for post in posts:
        like_filter = LikePost.objects.filter(post_id=post.id, username=request.user.username).first()
        post.is_liked_by_user = like_filter is not None

        comments_preview = post.comments.filter(parent__isnull=True).order_by('-created_at')[:3]
        for comment in comments_preview:
            comment.is_liked_by_user = comment.likes.filter(pk=request.user.pk).exists()
        post.comments_preview = comments_preview

    context = {
        'posts': posts,
    }

    return render(request, 'posts/home.html', context)

class PostDetailView(DetailView):
    model = Post

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['caption', 'image']
    success_url= '/'

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:   
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url= '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False

def about(request):
    return render(request, 'posts/about.html')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    success_url = '/'
    template_name = 'posts/post_upload.html'
    fields = ['caption', 'image']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def  like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        liked = True

    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        liked = False

    data = {
        'liked': liked,
        'likes_count': post.no_of_likes
    }
    return JsonResponse(data)