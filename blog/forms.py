from django import forms
from .models import Post, Comment, Tag

class PostForm(forms.ModelForm):

    tags = forms.MultipleChoiceField(choices=Tag.TAG_CHOICES)

    class Meta:
        model = Post
        fields = ['title', 'tags', 'content', 'thumbnail']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', 'parent_comment']