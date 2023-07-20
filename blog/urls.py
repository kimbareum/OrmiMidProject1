from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # 게시글
    path('', views.BlogIndex.as_view(), name='list'),
    path('write/', views.PostWrite.as_view(), name='write'),
    path('<int:post_id>/', views.PostDetail.as_view(), name='detail'),
    path('edit/<int:post_id>/', views.PostUpdate.as_view(), name='edit'),
    path('delete/<int:post_id>/', views.PostDelete.as_view(), name='delete'),
    path('<int:post_id>/like/', views.PostLike.as_view(), name='like'),
    # 코멘트
    path('<int:post_id>/comment/write/', views.CommentWrite.as_view(), name='cm-write'),
    path('comment/delete/<int:comment_id>/', views.CommentDelete.as_view(), name='cm-delete'),
    path('<int:post_id>/<int:comment_id>/like/', views.CommentLike.as_view(), name='cm-like'),
]