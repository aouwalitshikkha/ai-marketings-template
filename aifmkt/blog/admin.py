from django.contrib import admin
from .models import Category, Tag, Post, Placeholder, FAQ


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'indexable']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'indexable']
    prepopulated_fields = {'slug': ['name']}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_at', 'indexable']
    list_filter = ['status', 'category', 'created_at', 'indexable']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ['title']}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Content', {'fields': ['title', 'slug', 'body', 'short_answer']}),
        ('Taxonomy', {'fields': ['category', 'tags']}),
        ('Media', {'fields': ['featured_image']}),
        ('SEO', {'fields': ['meta_title', 'meta_description', 'indexable']}),
        ('Publishing', {'fields': ['status']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]


@admin.register(Placeholder)
class PlaceholderAdmin(admin.ModelAdmin):
    list_display = ['key', 'post', 'value']
    search_fields = ['key', 'post__title']
    list_filter = ['post']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'post', 'updated_at']
    search_fields = ['question', 'post__title']
    list_filter = ['post']
