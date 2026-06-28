from django.urls import path
from . import views

urlpatterns = [
    path("", views.CourseHubView.as_view(), name="course_list"),
    path("<slug:slug>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("<slug:course_slug>/<slug:chapter_slug>/", views.chapter_detail, name="chapter_detail"),
]
