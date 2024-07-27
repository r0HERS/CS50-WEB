from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User,Post,Follow,Like


def index(request):

    all_posts = Post.objects.all().order_by("id").reverse()

    paginator = Paginator(all_posts,10)

    page_number = request.GET.get('page')

    page_posts = paginator.get_page(page_number)

    user = request.user

    likes = Like.objects.all()

    liked_posts = []

    try:
        for like in likes:
            if like.user == user:
                liked_posts.append(like.post)
    except:
        liked_posts = []

    return render(request, "network/index.html",{
        "posts": all_posts,
        "page_posts": page_posts,
        "liked_posts": liked_posts,
        "likes": likes
    })

@csrf_exempt
def like(request,id):

    post = Post.objects.get(pk=id)
    user = request.user

    like = Like(
        post=post,
        user=user
    )

    like.save()

    return JsonResponse({'status': 'like success'})

@csrf_exempt
def unlike(request,id):

    post = Post.objects.get(pk=id)
    user = request.user
    like = Like.objects.get(post=post,user=user)
    
    like.delete()

    return JsonResponse({'status': 'unlike success'})

@login_required
def following_page(request):

    user = User.objects.get(id=request.user.id)
    following = Follow.objects.filter(following_user = user)
    all_posts = Post.objects.all().order_by("id").reverse()
    following_posts = []


    for post in all_posts:
        for person in following:
            if person.followed_user == post.user:
                following_posts.append(post)

    paginator = Paginator(following_posts,10)

    page_number = request.GET.get('page')

    page_posts = paginator.get_page(page_number)

    user = request.user

    likes = Like.objects.all()

    liked_posts = []

    try:
        for like in likes:
            if like.user == user:
                liked_posts.append(like.post)
    except:
        liked_posts = []

    return render(request, "network/following.html",{
        "posts": all_posts,
        "page_posts": page_posts,
        "liked_posts": liked_posts,
        "likes": likes
    })

@csrf_exempt
def edit_post(request, id):
        post =Post.objects.get(pk=id)
        data = json.loads(request.body)
        new_text = data.get('text')

        if new_text:
            post.text = new_text
            post.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No text.'}, status=400)

def add_post(request):

    if request.method == 'POST':
        text = request.POST['text']
        user = User.objects.get(id=request.user.id)

        new_post = Post(
            text = text,
            user = user
        )

    new_post.save()

    return HttpResponseRedirect(reverse("index"))

def profile(request,id):

    profile_user = User.objects.get(pk=id)

    all_posts = Post.objects.filter(user=profile_user).order_by("id").reverse()

    paginator = Paginator(all_posts,10)

    page_number = request.GET.get('page')

    page_posts = paginator.get_page(page_number)

    following = Follow.objects.filter(following_user = profile_user)
    
    followers = Follow.objects.filter(followed_user = profile_user)

    try:
        current_user = request.user

        follow = followers.filter(following_user = current_user)
    except:
        follow = None

    

    likes = Like.objects.all()

    liked_posts = []

    try:
        user = request.user
        for like in likes:
            if like.user == user:
                liked_posts.append(like.post)
    except:
        liked_posts = []


    return render(request,"network/profile.html",{
        "profile_user": profile_user,
        "page_posts": page_posts,
        "following": following,
        "followers": followers,
        "follow": follow,
        "liked_posts": liked_posts,
        "likes": likes
    })

def follow(request,id):

    user = request.user
    
    profile_user = User.objects.get(pk=id)

    followers = Follow.objects.filter(followed_user = profile_user)

    follow = followers.filter(following_user = user)
    
    if follow:
        a = Follow.objects.get(following_user = user, followed_user = profile_user)
        a.delete()
    else:
        follow = Follow(
            following_user = user,
            followed_user = profile_user
        )
        follow.save()

    return  HttpResponseRedirect(reverse("profile", args=(id, )))

    
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

