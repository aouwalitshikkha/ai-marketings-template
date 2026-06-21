from django.contrib import admin
from .models import GlossaryTerm, GlossaryPageConfig


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'status', 'review_score', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['term', 'short_definition', 'long_definition']
    readonly_fields = ['created_at', 'updated_at', 'version']
    fieldsets = [
        ('Term', {'fields': ['term', 'short_definition', 'long_definition']}),
        ('Details', {'fields': ['synonyms', 'acronym', 'example', 'use_cases', 'related_terms']}),
        ('Metadata', {'fields': ['sources', 'notes']}),
        ('Status', {'fields': ['status', 'review_score']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at', 'version']}),
    ]


@admin.register(GlossaryPageConfig)
class GlossaryPageConfigAdmin(admin.ModelAdmin):
    list_display = ['seo_title', 'updated_at']
