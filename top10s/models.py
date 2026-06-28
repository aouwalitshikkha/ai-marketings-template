from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.urls import reverse


class Profiles(models.Model):
    # Basic info
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # Content
    intro = RichTextField(blank=True, null=True)
    tldr = RichTextField(blank=True, null=True)
    conclusion = RichTextField(blank=True, null=True)

    # Comparison table (JSON)
    comparison_table = models.JSONField(blank=True, null=True)
    image = models.ImageField(upload_to="top/",  blank=True, null=True)
    # SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)


    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"slug": self.slug})


    # ---------------------------
    # 🔥 Replace [placeholder_key] dynamically
    # ---------------------------
    def render_field(self, text):
        if not text:
            return ""
    
        for ph in self.placeholders.all():
            ph_value = ph.get_placeholder_value()
    
            if ph_value is None:
                ph_value = ""
    
            # If image placeholder → center it with Tailwind
            if isinstance(ph_value, dict) and "url" in ph_value:
                ph_value = (
                    f'<img src="{ph_value["url"]}" '
                    f'alt="{ph_value.get("alt", ph.key)}" '
                    f'loading="lazy" class="mx-auto block">'
                )
    
            text = text.replace(f"[{ph.key}]", str(ph_value))
    
        return text


    # Public properties for template usage:
    @property
    def intro_html(self):
        return self.render_field(self.intro)

    @property
    def tldr_html(self):
        return self.render_field(self.tldr)

    @property
    def conclusion_html(self):
        return self.render_field(self.conclusion)

    def __str__(self):
        return self.title


# ----------------------------------
# 2. TOOL / SOFTWARE SECTION
# ----------------------------------
class Tool(models.Model):
    blog_post = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name="tools")

    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="tools/", blank=True, null=True)
    description = RichTextField()

    # Labels that YOU customize (Key Features, Pros, Advantages, Strengths, etc.)
    feature_label = models.CharField(max_length=100, default="Key Feature")
    features = models.TextField()

    pros_label = models.CharField(max_length=100, default="Pros")
    pros = models.TextField()
    

    personal_review = RichTextField()
    order = models.PositiveIntegerField(default=0, blank=True, null=True)


    def __str__(self):
        return self.name

    def features_list(self):
        return [f.strip() for f in self.features.split("\n") if f.strip()]

    def pros_list(self):
        return [p.strip() for p in self.pros.split("\n") if p.strip()]
        

       
class PlaceholderProfile(models.Model):
    profile = models.ForeignKey(
        Profiles, related_name='placeholders', on_delete=models.CASCADE
    )
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to='profile_placeholders/', blank=True, null=True)
    alt_text = models.CharField(max_length=150, blank=True, null=True)

    def get_placeholder_value(self):
        if self.image:
            return {
                "url": self.image.url,
                "alt": self.alt_text or self.key,
            }
        return self.value

    def __str__(self):
        return f"{self.key}: {self.value or 'Image Placeholder'}"