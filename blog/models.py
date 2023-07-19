from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    thumbnail = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.title}'


class PostFeeling(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_fixed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    depth = models.IntegerField(default=1)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.post.title}/{self.content}'


class CommentFeeling(models.Model):

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=True)


class Tag(models.Model):
    TAG_CHOICES = [
        ('Life', 'Life'),
        ('Style', 'Style'),
        ('Tech', 'Tech'),
        ('Sport', 'Sport'),
        ('Photo', 'Photo'),
        ('Develop', 'Develop'),
        ('Music', 'Music')
    ]
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=10, choices=TAG_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.post.title}/{self.name}'