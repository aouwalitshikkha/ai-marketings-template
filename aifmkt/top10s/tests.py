from django.test import TestCase, override_settings
from django.db import connection
from django.test.utils import CaptureQueriesContext
from .models import Profiles


class ProfileQueriesTest(TestCase):
    databases = "__all__"

    def test_profile_detail_prefetch(self):
        profile = Profiles.objects.first()
        if not profile:
            return
        with CaptureQueriesContext(connection) as ctx:
            p = Profiles.objects.prefetch_related("tools", "placeholders").get(pk=profile.pk)
            _ = list(p.tools.all())
            _ = p.render_field(p.intro)
            _ = p.render_field(p.tldr)
            _ = p.render_field(p.conclusion)
        self.assertLessEqual(len(ctx), 3,
            f"Expected <=3 queries with prefetch, got {len(ctx)}")
