from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # user = User.objects.filter(user__username__icontains=q)
    posts = Post.objects.filter(Q(user__username__icontains=q) |
                                Q(title__icontains=q) 
                                )
    # posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'home.html', context)


def postdetails(request, pk):
    postdetails = Post.objects.get(id=pk)
    context = {'postdetails':postdetails}
    return render(request, "postdetails.html", context)
 

@login_required(login_url='login')
def createPost(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'post_form.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def deletePost(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == "POST":
        post.delete()
        return redirect('home')
    context = {'obj':post}
    return render(request, 'delete.html')


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:   #user exists garxa vani login
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exists.')


    context = {'page': page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'login_register.html', {'form':form})


def profile(request, pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    context = {'user':user, 'posts':posts}
    return render(request, 'profile.html', context)
