from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'content', 'date_created')
    list_filter = ("status",)
    search_fields = ['title', 'content']


admin.site.register(Post, PostAdmin)