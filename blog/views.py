from django.shortcuts import render, redirect

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Post, Comment, Tag, PostFeeling, CommentFeeling
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm

import re

# Create your views here.


class BlogIndex(View):
    
    def get(self, request):
        posts = Post.objects.prefetch_related('tag_set')

        context = {
            "title": "블로그에 오신것을 환영합니다.",
            "posts": posts,
        }
        return render(request, 'blog/post_list.html', context)


class BlogError(View):
    
    def get(self,request):
        return render(request, 'blog/error.html')


class PostWrite(LoginRequiredMixin, View):

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

            tag_names = form.cleaned_data['tags'].split('#')[1:]
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if not tag_name:
                    continue
                try:
                    tag = Tag()
                    tag.name = tag_name
                    tag.writer = user
                    tag.post = post
                    tag.save()
                except:
                    messages.error(request, '태그가 정상적으로 입력되지 않았습니다.')
            return redirect('blog:list')
        messages.error(request, form.errors)
        return redirect('blog:write')


class PostDetail(View):
    
    def get(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('comment_set', 'tag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('blog:error')

        comments = post.comment_set.filter(depth=1)
        tags = post.tag_set.all()

        context = {
            "title": post.title,
            "post": post,
            "comments": comments,
            "tags": tags,
        }
        return render(request, 'blog/post_detail.html', context)


class PostUpdate(LoginRequiredMixin, View):

    def get(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('blog:error')
        
        tag_list = Tag.objects.filter(post=post)
        tags = ''
        for tag in tag_list:
            tags += (f'#{tag} ')
        post.tags = tags
        context = {
            "title": f'{post.title} 수정',
            "post": post,
        }
        return render(request, 'blog/post_edit.html', context)

    def post(self, request, post_id):
        form = PostForm(request.POST)
        try:
            post = Post.objects.prefetch_related('comment_set', 'tag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('blog:error')
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.thumbnail = form.cleaned_data['thumbnail']
            post.save()
            return redirect('blog:detail', post_id = post_id)
        messages.error(request, form.errors)
        return redirect('blog:edit', post_id=post_id)


class PostDelete(LoginRequiredMixin, View):

    def post(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('comment_set', 'tag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('blog:error')
        post.delete()
        return redirect('blog:list')


class CommentWrite(LoginRequiredMixin, View):
    
    def post(self, request, post_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            try:
                post = Post.objects.prefetch_related('comment_set', 'tag_set').get(pk=post_id)
            except ObjectDoesNotExist as e:
                messages.error(request, str(e))
                return redirect('blog:error')
            comment = form.save(commit=False)
            comment.writer = user
            comment.post = post
