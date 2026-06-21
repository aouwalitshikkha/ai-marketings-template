from django.contrib import admin
from .models import GlossaryTerm


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'slug', 'status', 'review_score', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['term', 'short_definition', 'long_definition']
    prepopulated_fields = {'slug': ['term']}
    readonly_fields = ['created_at', 'updated_at', 'version']
    fieldsets = [
        ('Term', {'fields': ['term', 'slug', 'short_definition', 'long_definition']}),
        ('Details', {'fields': ['synonyms', 'acronym', 'example', 'use_cases', 'related_terms']}),
        ('Metadata', {'fields': ['sources', 'notes']}),
        ('Status', {'fields': ['status', 'review_score']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at', 'version']}),
    ]
