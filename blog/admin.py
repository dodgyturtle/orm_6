from django.contrib import admin

from blog.models import Comment, Post, Tag


class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "post",
        "author",
        "published_at",
        "text",
    ]
    raw_id_fields = ["post", "author"]


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "published_at",
    ]
    raw_id_fields = ["likes", "tags"]


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
