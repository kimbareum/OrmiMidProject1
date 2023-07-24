from django.shortcuts import render, redirect
from django.http import Http404

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .models import Post, Comment, Tag, PostFeeling, CommentFeeling
from .forms import PostForm, CommentForm

from myapp.utils.utils import get_banner, view_count_cookie

from django.utils.decorators import method_decorator
from myapp.utils.decorator import is_user_own


# Create your views here.


class BlogIndex(View):
    
    def get(self, request):
        category_name = request.GET.get('category', None)
        page = int(request.GET.get('page', 0))
        sort = request.GET.get('sort', 'reverse')
        tag_list = list(map(lambda x: x[0], Tag.TAG_CHOICES))
        search_option = {
            "search_list" : {
                'normal': '생성시간▲',
                'reverse': '생성시간▼',
            },
            "category_name": category_name,
            "sort_option": sort,
        }

        q = Q(is_deleted=False)

        if category_name and category_name in tag_list:
            q &= Q(tag__name=category_name)
            title = f'{category_name} 검색 결과'
            banner = get_banner(main=f'{category_name} Blog')
        else:
            title = f'블로그에 오신것을 환영합니다.'
            banner = get_banner(main=f'Our Blog')

        if sort == 'normal':
            posts = Post.objects.prefetch_related('tag_set').filter(q).order_by('created_at')
        elif sort == 'reverse':
            posts = Post.objects.prefetch_related('tag_set').filter(q).order_by('-created_at')

        paginator = Paginator(posts, 6)
        try:
            page_object = paginator.page(page)
        except PageNotAnInteger:
            page_object = paginator.page(1)
        except EmptyPage:
            if page <= 0:
                page_object = paginator.page(1)
            else:
                page_object = paginator.page(paginator.num_pages)

        context = {
            "title": title,
            "banner": banner,
            "posts": page_object,
            "max_page": paginator.num_pages,
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
            raise Http404()
        
        cookie = view_count_cookie(request, post_id)

        if cookie.get('flag'):
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

        response = render(request, 'blog/post_detail.html', context)
        response.set_cookie('view_count', cookie.get('value'), expires=cookie.get('expire'))

        return response


@method_decorator(is_user_own, 'get')
@method_decorator(is_user_own, 'post')
class PostUpdate(LoginRequiredMixin, View):

    def get(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('tag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            raise Http404()
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
            raise Http404()
        
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


@method_decorator(is_user_own, 'post')
class PostDelete(LoginRequiredMixin, View):

    def post(self, request, post_id):
        try:
            post = Post.objects.prefetch_related('comment_set', 'tag_set').get(pk=post_id)
        except ObjectDoesNotExist as e:
            raise Http404()
        post.is_deleted = True
        post.save()
        return redirect('blog:list')


class PostLike(LoginRequiredMixin, View):

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist as e:
            raise Http404()
        
        user = request.user

        try:
            feeling = PostFeeling.objects.select_related('user').get(post=post, user=user)
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
                raise Http404()
            comment = form.save(commit=False)
            comment.writer = user
            comment.post = post
            if comment.parent_comment:
                comment.depth = comment.parent_comment.depth + 1
            else:
                comment.depth = 1
            comment.save()
        return redirect('blog:detail', post_id=post_id)


@method_decorator(is_user_own, 'post')
class CommentDelete(LoginRequiredMixin, View):

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            raise Http404()
        comment.is_deleted = True
        comment.save()
        return redirect('blog:detail', post_id=comment.post.pk)


class CommentLike(LoginRequiredMixin, View):

    def post(self, request, comment_id, post_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            raise Http404()
        
        user = request.user

        try:
            feeling = CommentFeeling.objects.select_related('user').get(comment=comment, user=user)
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