from django.urls import path
from . import views
# from blog.views import Index

app_name = 'blog'

urlpatterns = [
    # # 게시글
    path('', views.IndexBlog.as_view(), name='list'),
    # path('write/', views.Write.as_view(), name='write'),
    # path('<int:post_id>/', views.Detail.as_view(), name='detail'),
    # path('edit/<int:post_id>', views.Update.as_view(), name='edit'),
    # path('delete/<int:post_id>/', views.Delete.as_view(), name='delete'),
    # # 코멘트
    # path('<int:post_id>/comment/write', views.CommentWrite.as_view(), name='cm-write'),
    # path('comment/delete/<int:comment_id>', views.CommentDelete.as_view(), name='cm-delete'),
    # # 태그
    # path('<int:post_id>/tag/write', views.HashTagWrite.as_view(), name='tag-write'),
    # path('tag/delete/<int:hashTag_id>', views.HashTagDelete.as_view(), name='tag-delete'),
    # # 검색
    # path('search/<str:tag>', views.SearchTag,as_view(), name='tag-search'),
]