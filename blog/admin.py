from django.contrib import admin
from .models import Post, Author, Tag, Comment

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "comment_text")  # Fields shown in the list view

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tags", "date")    # Fields used for filtering
    list_display = ("title", "author", "date")  # Fields shown in the list view
    prepopulated_fields = {"slug": ("title",)}  # Automatically generate slug from title field

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment,CommentAdmin)

