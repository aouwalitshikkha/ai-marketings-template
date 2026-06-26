from django.contrib import admin
from .models import Profiles, Tool, PlaceholderProfile


class ToolInline(admin.TabularInline):
    model = Tool
    extra = 1
    ordering = ["order"]


class PlaceholderProfileInline(admin.TabularInline):
    model = PlaceholderProfile
    extra = 1


@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "created_at", "updated_at"]
    search_fields = ["title", "slug"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ToolInline, PlaceholderProfileInline]
    fieldsets = [
        ("Content", {"fields": ["title", "slug", "image", "intro", "tldr", "conclusion"]}),
        ("Comparison Table (JSON)", {"fields": ["comparison_table"], "classes": ["wide"]}),
        ("SEO", {"fields": ["meta_title", "meta_description"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"]}),
    ]


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ["name", "blog_post", "order"]
    list_filter = ["blog_post"]
    search_fields = ["name"]
    ordering = ["order"]


@admin.register(PlaceholderProfile)
class PlaceholderProfileAdmin(admin.ModelAdmin):
    list_display = ["key", "profile", "value"]
    search_fields = ["key", "profile__title"]
