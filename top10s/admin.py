from django.contrib import admin
from .models import Profiles, Tool, PlaceholderProfile


class ToolInline(admin.StackedInline):
    model = Tool
    extra = 1
    fields = [
        "name",
        "image",
        "description",
        "feature_label",
        "features",
        "pros_label",
        "pros",
        "personal_review",
    ]


class PlaceholderInline(admin.StackedInline):
    model = PlaceholderProfile
    extra = 1
    fields = [
        "key",
        "value",
        "image",
        "alt_text",
    ]
    classes = ("collapse",)


@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at", "updated_at",)
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ("Main Information", {
            "fields": (
                "title",
                "slug",
                "intro",
                "tldr",
                "conclusion",
                "image",
                "meta_title",
                "meta_description",
            ),
            "classes": ("wide",),
        }),

        ("Comparison Table", {
            "fields": ("comparison_table",),
            "classes": ("collapse",),
            "description": "Enter JSON formatted table. Example: { 'columns': [...], 'rows': [...] }"
        }),
    )

    inlines = [PlaceholderInline]


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "blog_post")
    search_fields = ("name",)


@admin.register(PlaceholderProfile)
class PlaceholderProfileAdmin(admin.ModelAdmin):
    list_display = ("key", "profile", "value")
    search_fields = ("key", "profile__title")
