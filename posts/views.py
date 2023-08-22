from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from . models import Post,LikePost,Comment
from django.contrib.auth.decorators import login_required
from django.views.generic import  CreateView, DetailView, UpdateView, DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

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
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(self.get_context_data(form=form))

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

def create_comment(request,post_id, parent_id=None):
    if request.method == 'POST':
       post = get_object_or_404(Post, id=post_id)
       text = request.POST.get('comment_text')
       author = request.user

       if parent_id:  #if parent_id is provided, then its a reply to a comment
           parent = get_object_or_404(Comment, id=parent_id)
           comment = Comment.objects.create(post=post,
                                             text=text, author=author, parent=parent)
           
       else:  #if parent_id is not provided, then its a comment on a post
           comment = Comment.objects.create(post=post,
                                             text=text, author=author)
           
       comment.save()
       return redirect('post-detail', post.id)
