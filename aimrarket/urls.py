"""
URL configuration for aimrarket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import index as sitemap_index, sitemap as sitemap_section
from rest_framework.authtoken.views import obtain_auth_token
from glossary.views import GlossaryMarkdownView
from .views import home_view, handler404_view, handler500_view
from .sitemaps import (
    StaticViewSitemap, BlogPostSitemap, CourseSitemap,
    ChapterSitemap, ProfilesSitemap, GlossaryTermSitemap,
)

handler404 = handler404_view
handler500 = handler500_view

sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogPostSitemap,
    "courses": CourseSitemap,
    "chapters": ChapterSitemap,
    "top10": ProfilesSitemap,
    "glossary": GlossaryTermSitemap,
}

urlpatterns = [
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap_index, {'sitemaps': sitemaps}, name='sitemap-index'),
    path('sitemap-<section>.xml', sitemap_section, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    re_path(r'^glossary\.md$', GlossaryMarkdownView.as_view(), name='glossary_markdown'),
    path('blog/', include('blog.urls')),
    path('glossary/', include('glossary.urls')),
    path('top/', include('top10s.urls')),
    path('hub/', include('courses.urls')),
    path('search/', include('search.urls')),
    path('', include('pages.urls')),
    path('api/', include('api.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', obtain_auth_token, name='api_token'),
]
