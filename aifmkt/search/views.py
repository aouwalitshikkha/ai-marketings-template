from django.db.models import Q
from django.shortcuts import render
from django.utils.html import strip_tags

from blog.models import Post
from top10s.models import Profiles


def _truncate(text, words=25):
    clean = strip_tags(text or "").strip()
    parts = clean.split()
    if len(parts) <= words:
        return clean
    return " ".join(parts[:words]) + "…"


def search_view(request):
    q = (request.GET.get("q") or "").strip()
    results = []

    if q:
        posts = (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .filter(
                Q(title__icontains=q)
                | Q(short_answer__icontains=q)
                | Q(body__icontains=q)
                | Q(category__name__icontains=q)
                | Q(tags__name__icontains=q)
            )
            .select_related("category")
            .distinct()
        )
        for post in posts:
            results.append({
                "title": post.title,
                "desc": _truncate(post.short_answer or post.body),
                "category": post.category.name if post.category else "Blog",
                "type": "Blog",
                "url": post.get_absolute_url(),
                "image": post.featured_image.url if post.featured_image else None,
                "slug": post.slug,
            })

        profiles = Profiles.objects.filter(
            Q(title__icontains=q)
            | Q(intro__icontains=q)
            | Q(tldr__icontains=q)
            | Q(conclusion__icontains=q)
        )
        for profile in profiles:
            results.append({
                "title": profile.title,
                "desc": _truncate(profile.intro or profile.tldr),
                "category": "Top 10",
                "type": "Top 10",
                "url": profile.get_absolute_url(),
                "image": profile.image.url if profile.image else None,
                "slug": profile.slug,
            })

    return render(request, "search/search.html", {"results": results, "q": q})
