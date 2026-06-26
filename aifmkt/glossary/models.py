from ckeditor.fields import RichTextField
from django.db import models
from django.db.models.functions import Lower


class GlossaryTerm(models.Model):
    term = models.CharField(max_length=255, unique=True)
    description = RichTextField()

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['term']
        indexes = [
            models.Index(fields=['status'], name='glossaryterm_status_idx'),
            models.Index(Lower('term'), name='glossaryterm_term_lower_idx'),
        ]

    def __str__(self):
        return self.term

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/glossary/#term-{self.pk}"


class GlossaryPageConfig(models.Model):
    seo_title = models.CharField(max_length=160, blank=True)
    seo_description = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Glossary Page Config"
        verbose_name_plural = "Glossary Page Config"

    def __str__(self):
        return self.seo_title or "Glossary Page Config"

