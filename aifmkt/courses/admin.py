from django.contrib import admin
from .models import Course, Chapter, Practice, ChecklistItem


class PracticeInline(admin.TabularInline):
    model = Practice
    extra = 1
    ordering = ["order"]


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1
    ordering = ["order"]


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    ordering = ["number"]
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "level", "category", "is_featured", "lessons_count", "created_at"]
    list_filter = ["level", "is_featured", "category"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ChapterInline]
    fieldsets = [
        ("Content", {"fields": ["title", "slug", "category", "description", "image", "level", "is_featured"]}),
        ("Course Body", {"fields": ["overview", "objectives", "requirements", "about"]}),
        ("SEO", {"fields": ["meta_title", "meta_description"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"]}),
    ]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "number", "status", "reading_time"]
    list_filter = ["status", "course"]
    search_fields = ["title", "summary", "content"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["created_at", "updated_at"]
    inlines = [PracticeInline, ChecklistItemInline]
    fieldsets = [
        ("Chapter", {"fields": ["course", "number", "title", "slug", "status", "published_date"]}),
        ("Content", {"fields": ["summary", "key_topics", "content"]}),
        ("SEO", {"fields": ["meta_title", "meta_description"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"]}),
    ]


@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ["title", "chapter", "order"]
    list_filter = ["chapter__course"]
    search_fields = ["title", "description"]


@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ["chapter", "order"]
    list_filter = ["chapter__course"]
