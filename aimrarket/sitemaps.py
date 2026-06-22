from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from courses.models import Course, Chapter
from top10s.models import Profiles
from glossary.models import GlossaryTerm


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return ["home", "blog_home", "profile_list", "course_list",
                "glossary_index", "about", "contact", "privacy", "search"]

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).order_by("-publish_date")

    def lastmod(self, obj):
        return obj.updated_at


class CourseSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Course.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class ChapterSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Chapter.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.updated_at


class ProfilesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Profiles.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class GlossaryTermSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return GlossaryTerm.objects.filter(status=GlossaryTerm.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at
