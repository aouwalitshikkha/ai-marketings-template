from django.contrib import admin
from .models import GlossaryCategory, GlossaryTerm, GlossaryPageConfig, GlossaryFAQ


@admin.register(GlossaryCategory)
class GlossaryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'slug', 'category', 'status', 'review_score', 'created_at', 'updated_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['term', 'short_definition', 'long_definition']
    prepopulated_fields = {'slug': ['term']}
    readonly_fields = ['created_at', 'updated_at', 'version']
    fieldsets = [
        ('Term', {'fields': ['term', 'slug', 'short_definition', 'long_definition']}),
        ('Classification', {'fields': ['category', 'synonyms', 'acronym']}),
        ('Details', {'fields': ['example', 'use_cases', 'related_terms']}),
        ('Metadata', {'fields': ['sources', 'notes']}),
        ('Status', {'fields': ['status', 'review_score']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at', 'version']}),
    ]


@admin.register(GlossaryPageConfig)
class GlossaryPageConfigAdmin(admin.ModelAdmin):
    list_display = ['title', 'json_ld_enabled', 'faq_enabled', 'updated_at']


@admin.register(GlossaryFAQ)
class GlossaryFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'page', 'order']
    list_filter = ['page']
    search_fields = ['question']
