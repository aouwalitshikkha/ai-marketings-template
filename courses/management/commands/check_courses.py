from django.core.management.base import BaseCommand
from courses.models import Course


class Command(BaseCommand):
    help = "List all courses"

    def handle(self, *args, **options):
        for c in Course.objects.all():
            self.stdout.write(f'{c.id}: "{c.title}" (level={c.level}, category="{c.category}", course_category={c.course_category})')
        if not Course.objects.exists():
            self.stdout.write(self.style.WARNING("No courses found in database."))
