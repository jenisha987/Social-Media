from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

# Create your views here.

def home(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'home.html', context)


def postdetails(request, pk):
    postdetails = Post.objects.get(id=pk)
    context = {'postdetails':postdetails}
    return render(request, "postdetails.html", context)


def createPost(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'post_form.html', context)


def updatePost(request, pk):
    postdetails = Post.objects.get(id=pk)
    form = PostForm(instance=postdetails)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=postdetails)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form':form}
    return render(request, 'post_form.html', context)


def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        post.delete()
        return redirect('home')
    context = {'obj':post}
    return render(request, 'delete.html')


