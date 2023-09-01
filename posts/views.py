from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.shortcuts import render, redirect
from . models import Post,LikePost,Comment,Reply
from django.contrib.auth.decorators import login_required
from django.views.generic import  CreateView, DetailView, UpdateView, DeleteView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        post = self.object
        comments_with_replies = []

        for comment in post.comments.all():
            replies_count = Reply.objects.filter()
            comment.replies_count = replies_count
            comments_with_replies.append(comment)

        context['comments_with_replies'] = comments_with_replies
        return context
   

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

def create_comment(request,post_id):
    if request.method == 'POST':
       post = get_object_or_404(Post, id=post_id)
       text = request.POST.get('comment_text')
       author = request.user
           
       comment = Comment.objects.create(post=post,
                                             text=text, author=author)
           
       comment.save()
       return redirect('post-detail', post.id)

def get_detailview_of_comment(request,post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)
    replies = Reply.objects.filter(comment=comment)
    
    return render(request, 'posts/comment_detail.html', {'comment': comment, 'post': post, 'replies': replies})

def create_reply(request, post_id, comment_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        text = request.POST.get('comment_text')
        author = request.user
        
        reply = Reply.objects.create(comment=comment, text=text, author=author, parent_reply=None)
        reply.save()
        return redirect('comment-detail', post_id=post.id, comment_id=comment.id)
    
def get_detailview_of_reply(request, post_id, comment_id, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    parent_reply = reply.parent_reply
    replies = Reply.objects.filter(comment=comment, parent_reply=reply).order_by('-created_at')
    
    
    return render(request, 'posts/reply_detail.html', {'reply': reply, 'post': post, 'comment': comment, 'replies': replies})




###This function is not working properly, I am trying to create a nested reply associated with the parent reply, i cant figure it out
def create_reply_to_another_reply(request, post_id, comment_id, parent_reply_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        parent_reply = get_object_or_404(Reply, id=parent_reply_id)
        text = request.POST.get('comment_text')
        author = request.user

        # Creating a nested reply associated with the parent reply
        nested_reply = Reply.objects.create(comment=comment, parent_reply=parent_reply, text=text, author=author)

        # Fetch all replies associated with the comment, including nested replies
        #replies = Reply.objects.filter(comment=comment)

        # Fetch the parent reply associated with the comment
        parent_reply = Reply.objects.filter(comment=comment, parent_reply=None)
        nested_reply.save()
        
        # Correct usage of reverse in get_detailview_of_reply
       # Correct usage of reverse in get_detailview_of_reply
        return redirect('reply-detail', post_id=post.id, comment_id=comment.id, reply_id=nested_reply.id)
        # return render(request, 'posts/reply_detail.html', {
        #     'post': post,
        #     'comment': comment,
        #     'parent_reply': parent_reply,
        #     'replies': replies,
        #     'nested_reply': nested_reply
        # })

def delete_reply_comment(request, post_id, comment_id, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    reply.delete()
    return redirect('comment-detail', post_id=post_id, comment_id=comment_id)