from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class UserProfile(models.Model):
#     user = models.OneToOneField(to="User", on_delete=models.CASCADE)
    


class Post(models.Model):
    content = models.TextField(null=False, blank=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def likes_count(self):
        # Like.objects.filter(post=self) = self.like_set
        return Like.objects.filter(post=self).count()

    def has_like(self, user):
        return Like.objects.filter(post=self, user=user).exists()

class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class Follower(models.Model):
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey('User', on_delete=models.CASCADE, related_name="followed")


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.CharField(max_length=255, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
