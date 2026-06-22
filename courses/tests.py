from django.test import TestCase
from django.db import connection
from django.test.utils import CaptureQueriesContext
from .models import Course


class CourseQueriesTest(TestCase):
    databases = "__all__"

    def test_course_list_prefetch(self):
        with CaptureQueriesContext(connection) as ctx:
            courses = Course.objects.prefetch_related("chapters").all()
            for c in courses:
                _ = c.lessons_count
                _ = c.duration
        self.assertLessEqual(len(ctx), 4,
            f"Expected <=4 queries with prefetch, got {len(ctx)}")
