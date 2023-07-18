from django.shortcuts import render, redirect

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Post, Comment, Tag, PostFeeling, CommentFeeling
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm

from myapp.utils.utils import get_banner


# Create your views here.


class BlogIndex(View):
    
    def get(self, request):
        category_name = request.GET.get('category', None)
        if category_name:
            posts = Post.objects.prefetch_related('tag_set').filter(tag__name=category_name, is_deleted=False)
            title = f'{category_name} 검색 결과'
            banner = get_banner(main=f'{category_name.capitalize()} Blog')
        else:
            posts = Post.objects.prefetch_related('tag_set').filter(is_deleted=False)
            title = "블로그에 오신것을 환영합니다."
            banner = get_banner()

        context = {
            "title": title,
            "banner": banner,
            "posts": posts,
        }
        return render(request, 'blog/post_list.html', context)


class BlogError(View):
    
    def get(self,request):
        context = {
            "banner": get_banner(text="Something Went Wrong..."),
        }
        return render(request, 'blog/error.html')


class PostWrite(LoginRequiredMixin, View):

    def get(self, request):
        form = PostForm()
        context = {
            "title": "게시글 작성하기",
            "banner": get_banner(),
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

        post.view_count += 1
        post.save()

        comments = post.comment_set.filter(depth=1)
        tags = post.tag_set.all()

        context = {
            "title": post.title,
            "banner": get_banner(),
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
            "banner": get_banner(),
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
        post.is_deleted = True
        post.save()
        return redirect('blog:list')


class CommentWrite(LoginRequiredMixin, View):
    
    def post(self, request, post_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            try:
                post = Post.objects.get(pk=post_id)
            except ObjectDoesNotExist as e:
                messages.error(request, str(e))
                return redirect('blog:error')
            comment = form.save(commit=False)
            comment.writer = user
            comment.post = post
            comment.depth = comment.parent_comment.depth + 1
            comment.save()
        return redirect('blog:detail', post_id=post_id)


class CommentDelete(LoginRequiredMixin, View):

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except ObjectDoesNotExist as e:
            messages.error(request, str(e))
            return redirect('blog:error')
        comment.is_deleted = True
        comment.save()
        return redirect('blog:detail', post_id=comment.post.pk)


class SearchCategory(View):
    
    def get(self, request):
        pass