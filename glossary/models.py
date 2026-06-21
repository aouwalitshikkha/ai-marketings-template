from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils.text import slugify


class GlossaryTerm(models.Model):
    term = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_definition = models.CharField(max_length=250)
    long_definition = models.TextField(blank=True)

    synonyms = models.CharField(max_length=500, blank=True)
    acronym = models.CharField(max_length=300, blank=True)

    example = models.TextField(blank=True)
    use_cases = models.TextField(blank=True)
    related_terms = models.ManyToManyField(
        'self', blank=True, symmetrical=True)

    sources = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PUBLISHED = 'PUBLISHED', 'Published'

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)
    review_score = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['term']
        indexes = [
            models.Index(fields=['slug'], name='glossaryterm_slug_idx'),
            models.Index(fields=['status'], name='glossaryterm_status_idx'),
            models.Index(Lower('term'), name='glossaryterm_term_lower_idx'),
        ]

    def __str__(self):
        return self.term

    def clean(self):
        if self.acronym:
            self.acronym = self.acronym.upper().strip()
        if self.synonyms:
            names = [s.strip() for s in self.synonyms.split(',') if s.strip()]
            for n in names:
                qs = GlossaryTerm.objects.exclude(
                    pk=self.pk).filter(term__iexact=n)
                if qs.exists():
                    raise ValidationError(
                        "A synonym matches an existing term name.")
                if self.term.lower().strip() == n.lower():
                    raise ValidationError(
                        "Synonyms cannot include the term itself.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.slug:
            base = slugify(self.term)
            slug = base
            i = 2
            while GlossaryTerm.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/glossary/#{self.slug}"



