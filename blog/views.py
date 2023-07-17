from django.shortcuts import render, redirect

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Post, Comment, Tag, PostFeeling, CommentFeeling
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm

# Create your views here.


class IndexBlog(View):
    
    def get(self, request):
        posts = Post.objects.all()
        context = {
            "title": "블로그에 오신것을 환영합니다.",
            "posts": posts,
        }
        return render(request, 'blog/post_list.html', context)


class Write(LoginRequiredMixin, View):

    def get(self, request):
        form = PostForm()
        context = {
            "title": "게시글 작성하기",
            'form': form,
        }
        return render(request, 'blog/post_form.html', context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            user = request.user
            post.writer = user
            post.save()
            return redirect('blog:list')
        messages.error(request, form.non_field_errors())
        return redirect('blog:write')


class Detail(View):
    
    def get(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('comment_set', 'tag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('blog:error')
        comments = post.comment
        tags = post.tag
        context = {
            "title": post.title,
            "post": post,
            "comments": comments,
            "tags": tags,
        }
        return render(request, 'blog/post_detail.html', context)


class Update(View):

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)


