from django.contrib import admin
from .models import Post, Comment, Tag, PostFeeling, CommentFeeling

# Register your models here.
admin.site.register(PostFeeling)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentFeeling)
admin.site.register(Tag)
