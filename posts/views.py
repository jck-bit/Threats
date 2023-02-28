from django.shortcuts import render, redirect
from . models import Post,LikePost
from django.contrib.auth.decorators import login_required
from django.views.generic import  CreateView, DetailView, UpdateView, DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

@login_required
def home(request):
    context ={
        'posts':Post.objects.all().order_by('-date_posted')
    }
    return render(request, 'posts/home.html', context)

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['caption', 'image']

    def form_valid(self, form):
        return super().form_valid(form)

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

        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()

        return redirect('/')
    