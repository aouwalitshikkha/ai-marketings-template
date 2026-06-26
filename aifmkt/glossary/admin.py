from django.contrib import admin
from .models import GlossaryTerm, GlossaryPageConfig


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['term', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Term', {'fields': ['term', 'description']}),
        ('Status', {'fields': ['status']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']}),
    ]


@admin.register(GlossaryPageConfig)
class GlossaryPageConfigAdmin(admin.ModelAdmin):
    list_display = ['seo_title', 'updated_at']
