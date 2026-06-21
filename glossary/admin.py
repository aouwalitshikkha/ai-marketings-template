from django.contrib import admin
from .models import GlossaryTerm, GlossaryPageConfig


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['term', 'short_definition', 'long_definition']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Term', {'fields': ['term', 'short_definition', 'long_definition']}),
        ('Status', {'fields': ['status']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]


@admin.register(GlossaryPageConfig)
class GlossaryPageConfigAdmin(admin.ModelAdmin):
    list_display = ['seo_title', 'updated_at']
