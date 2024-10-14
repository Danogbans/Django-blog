from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm, SignupForm, LoginForm
from blog.models import Post




#login_view: Handles user login.
def login_view(request):
    latest_posts = Post.objects.order_by('-created_at')[:4]
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'latest_posts': latest_posts})

    
# logout_view: Logs out the user.
def logout_view(request):
    logout(request)
    return redirect('post_list')


# signup_view: Handles user registration.
def signup_view(request):
    latest_posts = Post.objects.order_by('-created_at')[:4]
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.profile.email = form.cleaned_data.get('email')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form, 'latest_posts': latest_posts})


# profile_view: Displays and edits the user profile. Requires user log
@login_required
def profile_view(request):
    latest_posts = Post.objects.order_by('-created_at')[:4]
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'registration/profile.html', {'form': form, 'latest_posts': latest_posts})
