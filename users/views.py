from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from posts.models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from posts.models import LikePost,Follow
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import F
import random

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
    context_object_name = 'posts'
    
    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Post.objects.filter(user=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        context['profile_user'] = profile_user

        for post in context['posts']:
            like_filter = LikePost.objects.filter(post_id=post.id, username=self.request.user.username).first()
            post.is_liked_by_user = like_filter is not None

        context['post_queryset_length'] = Post.objects.filter(user=profile_user).count()
        following = Follow.objects.filter(follower=self.request.user, followed=profile_user).exists()
        context['profile_following'] = following      

        context['following'] = profile_user.following.all()
        context['followers'] = profile_user.followers.all()

        current_user = self.request.user
  
        return context

@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(user=user)
     
    for post in posts:
        like_filter = LikePost.objects.filter(post_id=post.id, username=user.username).first()
        post.is_liked_by_user = like_filter is not None
        

        following = Follow.objects.filter(follower=user).values_list('followed', flat=True).count()
        followers = Follow.objects.filter(followed=user).values_list('follower', flat=True).count()
 
    context = {
        'posts': posts,
        'post_queryset_length': posts.count(),
        'following': following,
        'followers': followers,

    }

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

@csrf_protect
@login_required
def follow_user(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    print(profile_user)

    if request.method == 'POST':
        if profile_user != request.user:
            follow, created = Follow.objects.get_or_create(follower=request.user, followed=profile_user)

            if not created:
                follow.delete()
                following = False
            else:
                following = True

            followers_count = profile_user.followers.count()
            following_count = profile_user.following.count()

            return JsonResponse({'following': following, 'followers_count': followers_count, 'following_count': following_count})
        else:
            return JsonResponse({'error': 'You cannot follow yourself'})
    else:
        return JsonResponse({'error': 'Something went wrong'})


@login_required
def suggested_users(request):
    # Get the  logged-in user
    user = request.user

    suggested_users = User.objects.filter(~Q(followers__follower=user) & ~Q(pk=user.pk)).order_by('?')[:4]
    data = list(suggested_users.values('id', 'username', profile_image_url=F('profile__image')))


    for user_data in data:
        user_data['profile_image_url'] = '/media/' + user_data['profile_image_url']

    data = random.sample(data, len(data))

    return JsonResponse({'users': data})