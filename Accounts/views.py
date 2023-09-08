from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Moderator
from .forms import *
from django.contrib.auth import authenticate, login, logout

# from .forms import PostForm, CommentForm


def mainpage(request):
    return render(request, 'index2.html')


def home(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form})


@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'comments.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def remove_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user.is_authenticated and (request.user == comment.author or request.user == comment.post.author or request.user.moderator):
        comment.delete()
    return redirect('post_detail', post_id=comment.post.id)


def add_comment_to_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})


def register(request):
    if request.method == 'POST':
        # Get user input data from the form
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Check if user with same username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully")
        return redirect('login')
    else:
        return render(request, 'reg.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            form = 'Invaild username or password'
            return render(request, 'Login1.html', {'form': form})
    else:

        return render(request, 'Login1.html')


def LogoutUser(request):
    logout(request)
    return redirect('login')
