from django.contrib import admin

# Register your models here.
from .models import User, Post, Like, Follower, Comment

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)
admin.site.register(Comment)