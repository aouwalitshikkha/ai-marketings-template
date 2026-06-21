import os
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from ckeditor.fields import RichTextField
from django.utils.html import format_html
from django.conf import settings



# --- Taxonomy Models ---
def get_placeholder_image_path(instance, filename):
    post_slug = instance.post.slug
    if not post_slug:
        post_slug = slugify(instance.post.title) or "default"
    filename = os.path.basename(filename)
    return f'blog/{post_slug}/{filename}'





class Category(models.Model):
    """
    Represents a blog post category.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the category."
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        help_text="A URL-friendly version of the name. Automatically generated."
    )
    description = models.TextField(
        blank=True,
        help_text="A brief description for the category page."
    )
    image = models.ImageField(
        upload_to='category_images/',
        blank=True,
        null=True,
        help_text="An optional image for the category."
    )
    
    indexable = models.BooleanField(
    default=False,
    help_text="If unchecked, adds 'noindex, nofollow' for this page."
    )


    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
        
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """
    Represents a tag that can be applied to blog posts.
    """
    name = models.CharField(
        max_length=100,
        unique=True
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        help_text="A URL-friendly version of the name. Automatically generated."
    )
    
    indexable = models.BooleanField(
    default=False,
    help_text="If unchecked, adds 'noindex, nofollow' for this page."
    )


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# --- Core Content Model ---

class Post(models.Model):
    """
    Represents a single blog post.
    """
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(
        max_length=250,
        help_text="The title of the blog post."
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,  # Changed to unique=True for the site/blog/slug/ URL structure
        help_text="A URL-friendly version of the title. Must be unique."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    # This is the field for your Django Rich Text Editor content
    body = RichTextField(
        help_text="The main content of the post. Use the rich text editor."
    )
    featured_image = models.ImageField(
        upload_to='post_images/',
        blank=True,
        null=True,
        help_text="An optional main image for the post."
    )

    # Taxonomy fields
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'
    )

    # Date and Status fields
    publish_date = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the post is published."
    )
    
    indexable = models.BooleanField(
    default=True,
    help_text="If unchecked, adds 'noindex, nofollow' for this page."
    )

    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )
    meta_title = models.CharField(
        max_length=255,
        blank=True, # Make it optional
        help_text="SEO Title: Appears in the browser tab and search results. Keep it under 60 characters."
    )
    meta_description = models.TextField(
        blank=True, # Make it optional
        help_text="SEO Description: A brief summary for search engines. Keep it under 160 characters."
    )
    short_answer = models.TextField(blank=True)

    # This connects the Post model to the generic comment system
    comments = GenericRelation('UserComment')

    class Meta:
        ordering = ['-publish_date']
        indexes = [
            models.Index(fields=['-publish_date']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def get_markdown_url(self):
        return reverse('post_markdown', kwargs={'slug': self.slug})
    
    def to_jsonld(self, request):
        
        if self.featured_image and hasattr(self.featured_image, "url"):
            image_url = request.build_absolute_uri(self.featured_image.url)
        else:
            image_url = "https://aiformarketings.com/static/images/default.jpg"

        
        data = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": request.build_absolute_uri(self.get_absolute_url())
            },
            "headline": self.meta_title or self.title,
            "description": self.meta_description or (self.short_answer or ""),
            "image": [image_url],
            "datePublished": self.publish_date.isoformat(),
            "dateModified": self.updated_at.isoformat(),
            "author": {
                "@type": "Person",
                "name": "Abdul Aouwal",
                "url": "https://www.facebook.com/itshikkha"
            },
            "publisher": {
                "@type": "Organization",
                "name": getattr(settings, "SITE_NAME", request.get_host())
            },
            "articleSection": self.category.name if self.category else None,
            "keywords": ", ".join(self.tags.values_list("name", flat=True))
        }
        # remove empty values
        return {k: v for k, v in data.items() if v not in [None, "", []]}
    
    def get_formatted_content(self):
        placeholders = self.placeholders.all()
        formatted_content = self.body
        for placeholder in placeholders:
            placeholder_value = placeholder.get_placeholder_value()
            if isinstance(placeholder_value, dict) and 'url' in placeholder_value:
                replacement_html = format_html(
                    '<figure class="flex justify-center"><img src="{}" loading="lazy" alt="{}" class="mx-auto"></figure>',
                    placeholder_value["url"],
                    placeholder_value.get("alt", placeholder.key)
                )
            else:
                replacement_html = str(placeholder_value or "")
            formatted_content = formatted_content.replace(f"[{placeholder.key}]", replacement_html)
        return formatted_content

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


# --- Reusable Commenting System ---

class UserComment(models.Model):
    """
    Final comment model supporting both authenticated and anonymous users.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # This is for LOGGED-IN users. It's optional.
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,  # Allows the field to be empty in the database
        blank=True  # Allows the field to be empty in forms/admin
    )

    # === THE FIX IS HERE ===
    # These fields MUST exist for the form to work.
    name = models.CharField(max_length=100, help_text="Name of the commenter.")
    email = models.EmailField(
        help_text="Email of the commenter (will not be published).")

    # Common fields
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(
        default=False,
        help_text="Comments must be approved to be visible."
    )

    # This field is for replies, which we are not implementing yet, but it's good to have.
    parent_comment = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = "User Comment"
        verbose_name_plural = "User Comments"

    def __str__(self):
        if self.author:
            return f"Comment by {self.author.username} on {self.content_object}"
        return f"Comment by {self.name} on {self.content_object}"
    

class Placeholder(models.Model):
    post = models.ForeignKey(Post, related_name='placeholders', on_delete=models.CASCADE)
    
    key = models.CharField(
        max_length=50,
        help_text="The unique key for the shortcode (e.g., 'circular_number'). Do not include brackets."
    )
    value = models.CharField(
        max_length=250,
        blank=True,
        null=True,
        help_text="The text value for this placeholder."
    )
    image = models.ImageField(
        upload_to=get_placeholder_image_path, # Use the function here
        blank=True,
        null=True,
        help_text="The image value for this placeholder. Will be saved in a folder named after the post's slug."
    )
    alt_text = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Alt text for the image."
    )

    def get_placeholder_value(self):
        if self.image and hasattr(self.image, 'url'):
            return {
                "url": self.image.url,
                "alt": self.alt_text or self.key  # Fallback to key for alt text
            }
        return self.value

    def __str__(self):
        return f"Placeholder for '{self.post.title}' -> [{self.key}]"

    class Meta:
        unique_together = ('post', 'key')


class FAQ(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="faqs"
    )
    question = models.CharField(max_length=255, help_text="The FAQ question.")
    answer = RichTextField(help_text="The answer to the FAQ question.")  # Rich editor
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update timestamp

    class Meta:
        ordering = ["-updated_at"]  # newest updated comes first

    def __str__(self):
        return f"FAQ for {self.post.title}: {self.question}"







