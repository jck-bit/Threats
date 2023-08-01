from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from posts.models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from posts.models import LikePost

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    #template_name = 'users/profile.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Post.objects.filter(user=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        context['profile_user'] = profile_user
        
        #adding the is_liked attribute to each post 
        for post in context['posts']:
            like_filter = LikePost.objects.filter(post_id=post.id, username=self.request.user.username).first()
            post.is_liked_by_user = like_filter is not None

        context['post_queryset_length'] = Post.objects.filter(user=profile_user).count()
        return context

@login_required
def profile(request):
    posts = Post.objects.filter(user=request.user)
    post_query_length = posts.count()
    context = {'posts':posts, 'post_query_length':post_query_length}
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f"Your account has been updated")
            return redirect('profile')
    
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/update.html', context)