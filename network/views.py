import json
import pdb
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone

from .models import User, Post, Follower, Like, Comment


# Index page method == GET
def post_index(request):
    # Pagination
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10) # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        liked_posts = [post for post in page_obj if post.has_like(request.user)]
    
        return render(request, "network/index.html", {
            "page_obj":page_obj,
            "liked_posts": liked_posts,
            "user": request.user,
        })
    else:
        return render(request, "network/index.html", {
        "page_obj":page_obj,
    })


# Index page method == POST
def post_create(request):
    # Pagination
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10) # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.user.is_authenticated:
        post = Post(
            content=request.POST.get("new-post-content"),
            user=request.user,
            timestamp=datetime.now(),
        )
        if not post.content:
            return render(request, "network/index.html", {
                "message": "Post content cannot be empty",
                "page_obj":page_obj,
            })
        else:
            post.save()
        return redirect("/")
            
    
def index(request):
    if request.method == "POST":
        return post_create(request)
    else:
        return post_index(request)


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


def profile(request, user_id):
    user = User.objects.get(pk=user_id)

    # Pagination
    posts = Post.objects.filter(user=user_id).order_by("-timestamp")
    paginator = Paginator(posts, 10) # show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "profile_user": user,
        "page_obj": page_obj,
        "followers": Follower.objects.filter(followed=user),
        "following": Follower.objects.filter(follower=user),
        "has_followed": Follower.objects.filter(follower=request.user, followed=user).exists(),  
    })


def follow(request, user_id):
    user = User.objects.get(pk=user_id)
    has_followed = Follower.objects.filter(follower=request.user, followed=user).exists()

    # If already followed, redirect
    if has_followed:
        return redirect(f"/users/{user_id}")
    # If hasn't followed, then follow 
    follower = Follower(
        follower = request.user,
        followed = user
    )
    follower.save()
    return redirect(f"/users/{user_id}")


def unfollow(request, user_id):
    user = User.objects.get(pk=user_id)
    Follower.objects.filter(follower=request.user, followed=user).delete()
    return redirect(f"/users/{user_id}")


def all_following_posts(request):
    # Prepare a followed list
    followed = [follower.followed for follower in Follower.objects.filter(follower=request.user)]

    # user__in=followed, filter users already in the followed list 
    posts = Post.objects.filter(user__in=followed).order_by('-timestamp')
    liked_posts = [post for post in posts if post.has_like(request.user)]

    # Pagination
    paginator = Paginator(posts, 10) # Show 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/all_following_posts.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts,
    })


def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "PUT":
        if request.user == post.user:
            post.content = json.loads(request.body)["content"]
            # timestamp is not real time update since used Ajax (no page refreshing), formatting on post.js savePostEdit function
            post.timestamp = timezone.now()
            post.save()
        return HttpResponse(status=200)

    if request.method == "DELETE":
        if request.user == post.user:
            post.delete()
        return HttpResponse(status=200)

    if request.method == "GET":
        return render(request, "network/index.html")
        

def toggle_like(request, post_id):
    
    post = Post.objects.get(pk=post_id)
    existing_like = Like.objects.filter(post=post, user=request.user).first()

    if existing_like:
        existing_like.delete()
    else:
        Like(
            post = post,
            user = request.user
        ).save()

    count = Like.objects.filter(post=post).count()
    return JsonResponse({"count": count, "liked": existing_like is None  })


# TODO       
def comments(request, post_id):
    pass