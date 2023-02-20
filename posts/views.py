from django.shortcuts import render, redirect
from . models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

@login_required
def upload(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image')
        caption = request.POST['caption']
        if image:
            new_post.image = image
        new_post = Post.objects.create(user=user, caption=caption, image=image)
        new_post.save()
        return redirect('/')
    else:
        return render(request, 'posts/post_upload.html')
