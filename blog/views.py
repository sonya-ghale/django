from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post
from .forms import PostForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import CustomLoginForm 

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Post
from .forms import PostForm

from .forms import CommentForm
from .models import Comment

def chrome_devtools_json(request):
    return JsonResponse({})

def home(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    return render(request, 'blog/home.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}")
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomLoginForm()

    return render(request, 'registration/custom_login_view.html', {'form': form})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(parent__isnull=True)
    form = CommentForm()  

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = Comment.objects.get(id=parent_id)
            comment.save()
            return redirect('post_detail', pk=pk)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'form': form,  
        'comments': comments,
    })


# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     if post.author != request.user:
#         return HttpResponseForbidden("You are not allowed to edit this post")
    
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES, instance=post)

#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#         else:
#             form = PostForm(instance=post)

#         return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk): 
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # usually redundant on edit, but OK
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else: 
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_edit.html', {'form': form})


# here create a form variable and pass it to the template context
@login_required
def post_new(request): 
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else: 
        form = PostForm()
# Postform instance (empty or filled with post data)
    
    return render(request, 'blog/post_edit.html', {'form': form})


def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'blog/goodbye.html')
    return redirect('post_list') 

# less safer 
# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     if post.author != request.user:
#         return HttpResponseForbidden("You are not allowed to delete this post.")
    
#     post.delete()
#     return redirect('post_list')

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=pk)