from django.db.models import Prefetch
from django.views.generic import ListView, DetailView
from .models import Profiles, Tool


class ProfileListView(ListView):
    model = Profiles
    template_name = "top10s/profile_list.html"
    context_object_name = "profiles"
    paginate_by = 6
    ordering = ["-created_at"]


class ProfileDetailView(DetailView):
    model = Profiles
    template_name = "top10s/profile_detail.html"
    context_object_name = "profile"

    def get_queryset(self):
        return Profiles.objects.prefetch_related(
            Prefetch("tools", queryset=Tool.objects.order_by("order")),
            "placeholders",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_profiles"] = Profiles.objects.exclude(pk=self.object.pk).order_by("-created_at")[:3]
        return context
