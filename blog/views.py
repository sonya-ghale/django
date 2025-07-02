from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse

def chrome_devtools_json(request):
    return JsonResponse({})

def home(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/home.html', {'posts': posts})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_edit(request, pk): 
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # form = PostForm(request.POST, instance=post, request.FILES)
        form = PostForm(request.POST, request.FILES, instance=post)  

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
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
