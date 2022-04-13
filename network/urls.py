
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("users/<int:user_id>", views.profile, name="profile"),
    path("users/<int:user_id>/follow", views.follow, name="follow"),
    path("users/<int:user_id>/unfollow", views.unfollow, name="unfollow"),
    path("users/following", views.all_following_posts, name="all_following_posts"),

    path("posts/<int:post_id>", views.edit_post, name="edit-post"),
    path("posts/<int:post_id>/toggle_like", views.toggle_like, name="toggle_like"),
    path("posts/<int:post_id>/comments", views.comments, name="comments"),
]
