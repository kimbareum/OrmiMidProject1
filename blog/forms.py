from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):

    tags = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Post
        fields = ['title', 'tags', 'content', 'thumbnail']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', 'parent_comment']