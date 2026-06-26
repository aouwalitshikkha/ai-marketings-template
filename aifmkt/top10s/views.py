from django.views.generic import ListView, DetailView
from .models import Profiles


class ProfileListView(ListView):
    model = Profiles
    template_name = "top10s/profile_list.html"
    context_object_name = "profiles"
    paginate_by = 6


class ProfileDetailView(DetailView):
    model = Profiles
    template_name = "top10s/profile_detail.html"
    context_object_name = "profile"

    def get_queryset(self):
        return Profiles.objects.prefetch_related("tools", "placeholders")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_profiles"] = Profiles.objects.exclude(pk=self.object.pk)[:3]
        return context
