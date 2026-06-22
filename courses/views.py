from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render
from .models import Course, Chapter


class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        qs = Course.objects.prefetch_related("chapters")
        level = self.request.GET.get("level")
        if level and level in ("Beginner", "Intermediate", "Advance"):
            qs = qs.filter(level=level)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_level"] = self.request.GET.get("level", "")
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        return Course.objects.prefetch_related("chapters")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        context["chapters"] = course.chapters.filter(status="published")
        context["related_courses"] = Course.objects.exclude(pk=course.pk)[:3]
        return context


def chapter_detail(request, course_slug, chapter_slug):
    course = get_object_or_404(Course, slug=course_slug)
    chapter = get_object_or_404(
        Chapter, course=course, slug=chapter_slug, status="published"
    )
    chapters = list(course.chapters.filter(status="published"))
    current_index = chapters.index(chapter) if chapter in chapters else 0
    prev_chapter = chapters[current_index - 1] if current_index > 0 else None
    next_chapter = chapters[current_index + 1] if current_index < len(chapters) - 1 else None

    context = {
        "course": course,
        "chapter": chapter,
        "chapters": chapters,
        "prev_chapter": prev_chapter,
        "next_chapter": next_chapter,
        "current_index": current_index + 1,
        "total_chapters": len(chapters),
    }
    return render(request, "courses/chapter_detail.html", context)
