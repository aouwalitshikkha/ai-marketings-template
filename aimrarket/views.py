from django.shortcuts import render

from blog.models import Post
from top10s.models import Profiles


def home_view(request):
    posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("category")
        .order_by("-publish_date")[:3]
    )
    profiles = Profiles.objects.order_by("-created_at")[:3]

    context = {
        "posts": posts,
        "profiles": profiles,
        "post_count": Post.objects.filter(status=Post.Status.PUBLISHED).count(),
        "profile_count": Profiles.objects.count(),
    }
    return render(request, "home.html", context)
