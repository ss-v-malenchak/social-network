from django.db import models
from django.contrib.auth.models import User
from .choices import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=50, blank=True, db_index=True, null=True)
    game_server = models.CharField(max_length=3, choices=SERVER_CHOICES, default='NON', null=True)
    game_race = models.CharField(max_length=2, choices=RACE_CHOICES, default='NN', null=True)
    game_alliance = models.CharField(max_length=50, blank=True, null=True)
    game_guild = models.CharField(max_length=50, blank=True, null=True)
    game_class = models.CharField(max_length=50, blank=True, null=True)
    character_equip_calculator = models.URLField(blank=True, default='', null=True)
    about_user = models.TextField(max_length=1024, blank=True, default='', null=True)
    # file will be saved to MEDIA_ROOT/uploads/2019/05/11
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, default='default.png')
    wallpaper = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, default='default.jpg')

    def __str__(self):
        return '{}'.format(self.user)

class Group(models.Model):
    name = models.CharField(max_length=50, blank=True, db_index=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    activities = models.TextField(max_length=1024, blank=True, default='', null=True)
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, default='default.png')
    wallpaper = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, default='default.jpg')

    def __str__(self):
        return '{}'.format(self.name)

class UserSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    subscription = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')

class GroupSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class UserPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, default='', null=True)
    text_content = models.TextField(max_length=1024, blank=True, default='', null=True)
    date_pub = models.DateTimeField(auto_now_add=True)

class UserPostFeedFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    feed = models.ForeignKey(UserPost, on_delete=models.CASCADE)

class UserPostLike(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserPostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1024, blank=True, default='', null=True)
    date_pub = models.DateTimeField(auto_now_add=True)

class UserPostCommentLike(models.Model):
    comment = models.ForeignKey(UserPostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class GroupPost(models.Model):
    author = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True, default='', null=True)
    text_content = models.TextField(max_length=1024, blank=True, default='', null=True)
    date_pub = models.DateTimeField(auto_now_add=True)

class GroupPostFeedFile(models.Model):
    file = models.FileField(upload_to="files/%Y/%m/%d")
    feed = models.ForeignKey(GroupPost, on_delete=models.CASCADE)

class GroupPostLike(models.Model):
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class GroupPostComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1024, blank=True, default='', null=True)
    date_pub = models.DateTimeField(auto_now_add=True)

class GroupPostCommentLike(models.Model):
    comment = models.ForeignKey(GroupPostComment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)