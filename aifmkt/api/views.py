from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from glossary.models import GlossaryTerm, GlossaryPageConfig
from blog.models import Post, Category, Tag
from courses.models import Course, Chapter
from top10s.models import Profiles
from .serializers import (
    GlossaryTermSerializer, GlossaryTermListSerializer, GlossaryPageConfigSerializer,
    PostListSerializer, PostDetailSerializer, CategorySerializer, TagSerializer,
    CourseListSerializer, CourseDetailSerializer, ChapterSerializer,
    ProfilesListSerializer, ProfilesDetailSerializer,
)


# ── Glossary ──

class GlossaryTermViewSet(viewsets.ModelViewSet):
    queryset = GlossaryTerm.objects.all().order_by('term')
    serializer_class = GlossaryTermSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['term', 'description']
    ordering_fields = ['term', 'created_at', 'updated_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return GlossaryTermListSerializer
        return GlossaryTermSerializer


class GlossaryPageConfigViewSet(viewsets.ModelViewSet):
    queryset = GlossaryPageConfig.objects.all()
    serializer_class = GlossaryPageConfigSerializer


# ── Blog ──

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'category').prefetch_related('tags', 'faqs').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category__slug', 'author']
    search_fields = ['title', 'short_answer', 'body']
    ordering_fields = ['publish_date', 'created_at', 'updated_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            return qs.only(
                'id', 'title', 'slug', 'author', 'category', 'status',
                'short_answer', 'publish_date', 'created_at', 'updated_at',
                'featured_image', 'meta_title', 'meta_description',
            )
        return qs


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


# ── Courses ──

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.prefetch_related('chapters').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['level', 'is_featured', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseListSerializer
        return CourseDetailSerializer


class ChapterViewSet(viewsets.ModelViewSet):
    queryset = Chapter.objects.prefetch_related('practices', 'checklist_items').all()
    serializer_class = ChapterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course__slug', 'status']
    search_fields = ['title', 'summary', 'content']
    ordering_fields = ['number', 'created_at', 'updated_at']


# ── Top 10 ──

class ProfilesViewSet(viewsets.ModelViewSet):
    queryset = Profiles.objects.prefetch_related('tools').all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfilesListSerializer
        return ProfilesDetailSerializer
