from django.shortcuts import render, redirect

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

from django.contrib.auth import get_user_model
from .models import Post, Comment, Tag, PostFeeling, CommentFeeling
from .forms import PostForm, CommentForm

from myapp.utils.utils import get_banner, user_check

import re


# Create your views here.

### 공용페이지
# class BlogIndex(View):
    
#     def get(self, request):
#         page = request.GET.get('page')
#         posts = Post.objects.prefetch_related('tag_set').filter(is_deleted=False).order_by('-created_at')
#         paginator = Paginator(posts, 6)
#         try:
#             page_object = paginator.page(page)
#         except PageNotAnInteger:
#             page_object = paginator.page(1)
#         except EmptyPage:
#             page_object = paginator.page(paginator.num_pages)
#         title = "블로그에 오신것을 환영합니다."
#         banner = get_banner()

#         tag_list = list(map(lambda x: x[0], Tag.TAG_CHOICES))

#         search_option = {
#             "search_list" : {
#                 'normal': '생성시간▲',
#                 'reverse': '생성시간▼',
#             },
#         }

#         context = {
#             "title": title,
#             "banner": banner,
#             "posts": page_object,
#             "paginator": paginator,
#             "tag_list": tag_list,
#             "search_option": search_option,
#         }
#         return render(request, 'blog/post_list.html', context)


class BlogIndex(View):
    
    def get(self, request):
        category_name = request.GET.get('category', None)
        page = request.GET.get('page', None)
        sort = request.GET.get('sort', None)
        tag_list = list(map(lambda x: x[0], Tag.TAG_CHOICES))
        search_option = {
            "search_list" : {
                'normal': '생성시간▲',
                'reverse': '생성시간▼',
            },
            "category_name": category_name,
            "sort_option": sort,
        }

        if category_name and category_name in tag_list:
            posts = Post.objects.prefetch_related('tag_set').filter(tag__name=category_name, is_deleted=False)
            title = f'{category_name} 검색 결과'
            banner = get_banner(main=f'{category_name} Blog')
        else:
            posts = Post.objects.prefetch_related('tag_set').filter(is_deleted=False)
            title = f'블로그에 오신것을 환영합니다.'
            banner = get_banner(main=f'Our Blog')

        if sort == 'normal':
            posts = posts.order_by('created_at')
        elif sort == 'reverse':
            posts = posts.order_by('-created_at')

        paginator = Paginator(posts, 6)
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            page_object = paginator.page(paginator.num_pages)

        context = {
            "title": title,
            "banner": banner,
            "posts": page_object,
            "paginator": paginator,
            "tag_list": tag_list,
            "search_option": search_option,
        }
        return render(request, 'blog/post_list.html', context)


### 포스트
class PostWrite(LoginRequiredMixin, View):

    def get(self, request):
        tag_list = list(map(lambda x: x[0], Tag.TAG_CHOICES))
        context = {
            "title": "게시글 작성하기",
            "banner": get_banner(),
            'tag_list': tag_list,
        }
        return render(request, 'blog/post_form.html', context)
    
    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            user = request.user
            post = Post.objects.create(
                writer=user,
                title=form.cleaned_data['title'],
                content=form.cleaned_data['content'],
                thumbnail=form.cleaned_data['thumbnail']
                )
            tag_names = form.cleaned_data['tags']
            for tag in tag_names:
                Tag.objects.create(name=tag, post=post)
            return redirect('blog:list')
        messages.error(request, form.errors)
        return redirect('blog:write')


class PostDetail(View):
    
    def get(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('comment_set', 'tag_set', 'postfeeling_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('error')
        post.view_count += 1
        post.save()
        if request.user.is_authenticated:
            user_feeling_post = post.postfeeling_set.filter(user=request.user)
            is_like_post = True if user_feeling_post and user_feeling_post[0].like == True else False
            like_comment_list = Comment.objects.filter(
                post=post,
                commentfeeling__user=request.user,
                commentfeeling__like=True
            ).values_list('pk', flat=True)
        else:
            is_like_post = False
            like_comment_list = []
        
        comments = post.comment_set.filter(depth=1)
        tags = post.tag_set.all()
        
        context = {
            "title": post.title,
            "banner": get_banner(),
            "post": post,
            "comments": comments,
            "tags": tags,
            "is_like_post": is_like_post,
            "like_comment_list": like_comment_list,
        }
        return render(request, 'blog/post_detail.html', context)


class PostUpdate(LoginRequiredMixin, View):

    def get(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('tag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('error')
        tag_list = list(map(lambda x: x[0], Tag.TAG_CHOICES))
        tags = post.tag_set.all()
        selected_tag_list = []
        for tag in tags:
            selected_tag_list.append(tag.name)
        context = {
            "title": f'{post.title} 수정',
            "banner": get_banner(),
            "post": post,
            "tag_list": tag_list,
            "selected_tag_list": selected_tag_list,
        }
        return render(request, 'blog/post_edit.html', context)

    def post(self, request, post_id):
        form = PostForm(request.POST)
        try:
            post = Post.objects.prefetch_related('tag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('error')
        if not user_check(post.writer, request.user):
            messages.error(request, "현재 로그인된 계정을 확인해주세요.")
            return redirect('error')
        
        if form.is_valid():
            post.title = form.cleaned_data['title']
            post.content = form.cleaned_data['content']
            post.thumbnail = form.cleaned_data['thumbnail']
            post.save()
            update_tags = form.cleaned_data['tags']
            current_tags = post.tag_set.all()
            for tag_name in update_tags:
                Tag.objects.get_or_create(name=tag_name, post_id=post_id)
            for tag in current_tags:
                if tag.name not in update_tags:
                    tag.delete()
            return redirect('blog:detail', post_id = post_id)
        messages.error(request, form.errors)
        return redirect('blog:edit', post_id=post_id)


class PostDelete(LoginRequiredMixin, View):

    def post(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('comment_set', 'tag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('error')
        if not user_check(post.writer, request.user):
            messages.error(request, "현재 로그인된 계정을 확인해주세요.")
            return redirect('error')
        post.is_deleted = True
        post.save()
        return redirect('blog:list')


class PostLike(LoginRequiredMixin, View):

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('error')
        
        user = request.user

        try:
            feeling = PostFeeling.objects.select_related('user').get(post=post)
            like = feeling.like
            if like:
                post.like_count -= 1
            else:
                post.like_count += 1
            post.save()
            feeling.like = not like
            feeling.save()
        except:
            PostFeeling.objects.create(user=user, post=post)
            post.like_count += 1
            post.save()

        return redirect('blog:detail', post_id=post_id)

### 코멘트
class CommentWrite(LoginRequiredMixin, View):
    
    def post(self, request, post_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            try:
                post = Post.objects.get(pk=post_id)
            except ObjectDoesNotExist as e:
                messages.error(request, str(e))
                return redirect('error')
            comment = form.save(commit=False)
            comment.writer = user
            comment.post = post
            if comment.parent_comment:
                comment.depth = comment.parent_comment.depth + 1
            else:
                comment.depth = 1
            comment.save()
        return redirect('blog:detail', post_id=post_id)


class CommentDelete(LoginRequiredMixin, View):

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('error')
        if not user_check(comment.writer, request.user):
            messages.error(request, "현재 로그인된 계정을 확인해주세요.")
            return redirect('error')
        comment.is_deleted = True
        comment.save()
        return redirect('blog:detail', post_id=comment.post.pk)


class CommentLike(LoginRequiredMixin, View):

    def post(self, request, comment_id, post_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('error')
        
        user = request.user

        try:
            feeling = CommentFeeling.objects.select_related('user').get(comment=comment)
            like = feeling.like
            if like:
                comment.like_count -= 1
            else:
                comment.like_count += 1
            comment.save()
            feeling.like = not like
            feeling.save()
        except:
            CommentFeeling.objects.create(user=user, comment=comment)
            comment.like_count += 1
            comment.save()

        return redirect('blog:detail', post_id=post_id)