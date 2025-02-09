from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Post,Author
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def register(request):
    # If the request is a POST request, process the form data
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'blog/register.html')

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        # Authenticate and log the user in
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('login')  # Redirect to the login page after registration
    
    # If not a POST request, render the registration form
    return render(request, 'blog/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

@login_required
def starting_page(request):
    latest_posts = Post.objects.all().order_by('-date')[:3]
    return render(request, "blog/index.html", {"posts": latest_posts})

@login_required
def posts(request):  # Renamed function to avoid conflict
    all_posts = Post.objects.all()
    return render(request, "blog/all-post.html", {"all_posts": all_posts})
@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            # comment.author = request.user.author  # Assumes a relationship between user and author
            comment.save()
            return redirect('post-detail-page', slug=slug)
    else:
        form = CommentForm()
    
    return render(request, "blog/post-detail.html", {
        "post": post,
        "post_tags": post.tags.all(),
        "form": form
    })
