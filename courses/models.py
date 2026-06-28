from django.db import models
from django.utils.text import slugify
import math
from django.urls import reverse


class CourseCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, help_text="What you'll learn blurb for the hub section")
    icon = models.CharField(max_length=50, blank=True, help_text="Emoji or icon label for the category")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Course categories"

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    course_category = models.ForeignKey(
        CourseCategory, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='courses'
    )
    is_featured = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    level = models.CharField(
        max_length=20,
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advance', 'Advance')],
        default='Beginner',
        db_index=True
    )
    meta_title = models.CharField(max_length=255, blank=True, help_text="Custom meta title for SEO.")
    meta_description = models.TextField(blank=True, help_text="Custom meta description for SEO.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    overview = models.TextField(blank=True)
    objectives = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    about = models.TextField(blank=True)
    image = models.ImageField(upload_to='courses/images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_meta_title(self):
        return self.meta_title or self.title

    def get_meta_description(self):
        return self.meta_description or (self.description[:155] if self.description else '')

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    @property
    def lessons_count(self):
        return self.chapters.count()

    @property
    def duration(self):
        total_minutes = 0
        for chapter in self.chapters.all():
            minutes = chapter.reading_time
            if isinstance(minutes, int):
                total_minutes += minutes
        hours = total_minutes // 60
        minutes = total_minutes % 60
        if hours:
            return f"{hours}h {minutes}m" if minutes else f"{hours}h"
        return f"{minutes}m"

    def __str__(self):
        return self.title


class Chapter(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    key_topics = models.TextField(blank=True)
    content = models.TextField(blank=True)
    meta_title = models.CharField(max_length=255, blank=True, help_text="Custom meta title for SEO.")
    meta_description = models.TextField(blank=True, help_text="Custom meta description for SEO.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Chapter.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base_slug}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "chapter_detail",
            kwargs={"course_slug": self.course.slug, "chapter_slug": self.slug}
        )

    @property
    def reading_time(self):
        texts = [
            self.summary or '',
            self.key_topics or '',
            self.content or '',
        ]
        for practice in self.practices.all():
            texts.append(practice.description or '')
            texts.append(practice.tip or '')
        for item in self.checklist_items.all():
            texts.append(item.description or '')
        words = 0
        for text in texts:
            words += len(text.split())
        if not words:
            return 0
        return math.ceil(words / 200)

    def get_meta_title(self):
        if self.meta_title:
            return self.meta_title
        return f'{self.title} – {self.course.title}'

    def get_meta_description(self):
        return self.meta_description or (self.summary[:155] if self.summary else '')

    class Meta:
        ordering = ['number', 'created_at']

    def __str__(self):
        return f'{self.course.title} – Chapter {self.number}: {self.title}'


class Practice(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='practices', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    tip = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        if self.title:
            return f'{self.chapter} – Practice {self.title}'
        return f'{self.chapter} – Practice'


class ChecklistItem(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='checklist_items', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'{self.chapter} – Checklist Item'
