from django.contrib import admin
from .models import Category, Post, Author, PostCategory, Comment, CategorySubscribers
from modeltranslation.admin import TranslationAdmin

class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(CategorySubscribers)
