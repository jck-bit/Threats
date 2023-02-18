from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm
from posts.models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

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
    # template_name = 'users/profile.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return Post.objects.filter(user=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return context


def profile(request):
    posts = Post.objects.filter(user=request.user)
    context = {'posts':posts}
    return render(request, 'users/profile.html', context)