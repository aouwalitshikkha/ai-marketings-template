from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'glossary/terms', views.GlossaryTermViewSet)
router.register(r'glossary/page-config', views.GlossaryPageConfigViewSet)
router.register(r'blog/posts', views.PostViewSet)
router.register(r'blog/categories', views.CategoryViewSet)
router.register(r'blog/tags', views.TagViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'chapters', views.ChapterViewSet)
router.register(r'blog/placeholders', views.PlaceholderViewSet)
router.register(r'top10s', views.ProfilesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
