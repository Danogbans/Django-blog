from django.contrib import admin
from .models import Post, Comment

# Admin interface for the Post and Comment models, Customizes the display, search, and filter options for posts and comments.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'category', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('category', 'author', 'updated_at', 'created_at')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    ordering = ('created_at',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content',)
    list_filter = ('post', 'author', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)