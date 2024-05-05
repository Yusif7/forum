from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import CustomUserCreationForm, PostForm, CommentForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import logout, login, authenticate
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        return render(request, 'forum/allposts.html')
    else:
        return render(request, 'forum/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'forum/signupuser.html', {'form': CustomUserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('allposts')
            except IntegrityError:
                return render(request, 'forum/signupuser.html', {'form': CustomUserCreationForm(),
                                                                 'error': 'Это имя пользователя уже занято. Пожалуйста, выберите новое имя пользователя!'})
        else:
            return render(request, 'forum/signupuser.html',
                          {'form': CustomUserCreationForm(), 'error': 'Пароли не совпадают!'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'forum/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'forum/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Имя пользователя и пароль не совпадают!'})
        else:
            login(request, user)
            return redirect('allposts')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def owneruser(request):
    return render(request, 'forum/owneruser.html')


@login_required
def createpost(request):
    if request.method == 'GET':
        return render(request, 'forum/createpost.html', {'form': PostForm()})
    else:
        try:
            form = PostForm(request.POST)
            newPost = form.save(commit=False)
            newPost.user = request.user
            newPost.save()
            return redirect('allposts')
        except ValueError:
            return render(request, 'forum/createpost.html',
                          {'form': PostForm(), 'error': 'Bad data passed in, try again please!'})


@login_required
def allposts(request):
    posts = Post.objects.filter(date_completed__isnull=True).order_by('-date_created')
    return render(request, 'forum/allposts.html', {'posts': posts})


@login_required
def ownerposts(request):
    posts = Post.objects.filter(date_completed__isnull=True, user=request.user).order_by('-date_completed')
    return render(request, 'forum/ownerposts.html', {'posts': posts})


@login_required
def controlposts(request):
    posts = Post.objects.filter(date_completed__isnull=True).order_by('-date_completed')
    return render(request, 'forum/controlposts.html', {'posts': posts})


@login_required
def viewpost(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    user_comment = Comment.objects.filter(post=post)
    previous_url = request.META.get('HTTP_REFERER', '')
    urls = [
        {
            'allposts_url': '/posts/',
            'owner_url': '/myposts/',
            'previous_url_allposts': previous_url[-len('/posts/'):],
            'previous_url_owner': previous_url[-len('/myposts/'):],
        }
    ]
    if request.method == 'GET':
        form = PostForm(instance=post)
        commentForm = CommentForm()
        return render(request, 'forum/viewpost.html',
                      {'post': post, 'form': form, 'urls': urls, 'user_comment': user_comment,
                       'commentForm': commentForm})
    else:
        try:
            user_comment = CommentForm(request.POST)
            if user_comment.is_valid():
                comment = user_comment.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('viewpost', post_pk=post_pk)

            form = PostForm(request.POST, instance=post)
            form.save()
            return redirect('allposts')
        except ValueError:
            return render(request, 'forum/viewpost.html',
                          {'post': post, 'form': form, 'user_comment': user_comment, 'error': 'Bad info'})


@login_required
def completepost(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        post.date_completed = timezone.now()
        post.save()
        return redirect('allposts')


@login_required
def completedposts(request):
    posts = Post.objects.filter(date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'forum/completedposts.html', {'posts': posts})


@login_required
def deletepost(request, post_pk):
    if request.user.last_name == 'Патриарх':
        todo = get_object_or_404(Post, pk=post_pk)
        if request.method == 'POST':
            todo.delete()
            return redirect('allposts')
    else:
        todo = get_object_or_404(Post, pk=post_pk, user=request.user)
        if request.method == 'POST':
            todo.delete()
            return redirect('allposts')


@login_required
def addcomment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    commentForm = CommentForm(instance=post)
    if request.method == 'GET':
        return render(request, 'forum/viewpost.html',
                      {'commentForm': commentForm})


def delete_comment(request, comment_id, post_pk):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.last_name == "Патриарх" or request.user.last_name == "Владыка" or request.user.last_name == "Палач":
        comment.delete()
    return redirect('viewpost', post_pk=post_pk)

