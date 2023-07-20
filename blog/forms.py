from django import forms
from .models import Post, Comment, Tag

import re

class PostForm(forms.ModelForm):

    tags = forms.MultipleChoiceField(choices=Tag.TAG_CHOICES)

    class Meta:
        model = Post
        fields = ['title', 'tags', 'content', 'thumbnail']

    def is_valid(self):
        valid = super().is_valid()

        if not valid:
            return False

        p = re.compile(r'<script[^>]*>.*?<\/script[^>]*>', re.DOTALL)
        self.cleaned_data['content']= p.sub(' ' , self.cleaned_data['content'])

        return True


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content', 'parent_comment']