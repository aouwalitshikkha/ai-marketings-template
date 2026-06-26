from rest_framework import serializers
from glossary.models import GlossaryTerm, GlossaryPageConfig
from blog.models import Post, Category, Tag, FAQ
from courses.models import Course, Chapter, Practice, ChecklistItem
from top10s.models import Profiles, Tool


# ── Glossary ──

class GlossaryTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryTerm
        fields = ['id', 'term', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class GlossaryTermListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryTerm
        fields = ['id', 'term', 'status', 'created_at']


class GlossaryPageConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryPageConfig
        fields = ['id', 'seo_title', 'seo_description', 'updated_at']
        read_only_fields = ['id', 'updated_at']


# ── Blog ──

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'indexable']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'indexable']
        read_only_fields = ['id']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class PostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    tags = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author_name', 'category_name', 'tags',
            'short_answer', 'status', 'publish_date', 'created_at', 'updated_at',
            'featured_image', 'meta_title', 'meta_description',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'publish_date']


class PostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    faqs = FAQSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author_name', 'body', 'category', 'tags',
            'short_answer', 'status', 'publish_date', 'created_at', 'updated_at',
            'featured_image', 'meta_title', 'meta_description', 'faqs',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'publish_date']


# ── Courses ──

class PracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Practice
        fields = ['id', 'title', 'description', 'tip', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['id', 'description', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChapterSerializer(serializers.ModelSerializer):
    practices = PracticeSerializer(many=True, read_only=True)
    checklist_items = ChecklistItemSerializer(many=True, read_only=True)
    reading_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chapter
        fields = [
            'id', 'course', 'number', 'title', 'slug', 'summary',
            'content', 'key_topics', 'status', 'reading_time',
            'practices', 'checklist_items',
            'meta_title', 'meta_description',
            'published_date', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChapterListSerializer(serializers.ModelSerializer):
    reading_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chapter
        fields = [
            'id', 'course', 'number', 'title', 'slug', 'summary',
            'key_topics', 'status', 'reading_time',
            'meta_title', 'meta_description', 'published_date',
        ]
        read_only_fields = ['id']


class CourseListSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(read_only=True)
    duration = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'level',
            'category', 'is_featured', 'lessons_count', 'duration',
            'image', 'meta_title', 'meta_description',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseDetailSerializer(serializers.ModelSerializer):
    chapters = ChapterListSerializer(many=True, read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)
    duration = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'level',
            'category', 'is_featured', 'lessons_count', 'duration',
            'overview', 'objectives', 'requirements', 'about',
            'image', 'chapters',
            'meta_title', 'meta_description',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ── Top 10 ──

class ToolSerializer(serializers.ModelSerializer):
    features_list = serializers.SerializerMethodField()
    pros_list = serializers.SerializerMethodField()

    class Meta:
        model = Tool
        fields = [
            'id', 'name', 'image', 'description',
            'feature_label', 'features', 'features_list',
            'pros_label', 'pros', 'pros_list',
            'personal_review', 'order',
        ]
        read_only_fields = ['id']

    def get_features_list(self, obj):
        return obj.features_list()

    def get_pros_list(self, obj):
        return obj.pros_list()


class ProfilesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = [
            'id', 'title', 'slug', 'image',
            'meta_title', 'meta_description',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProfilesDetailSerializer(serializers.ModelSerializer):
    tools = ToolSerializer(many=True, read_only=True)

    class Meta:
        model = Profiles
        fields = [
            'id', 'title', 'slug', 'intro', 'tldr', 'conclusion',
            'comparison_table', 'image', 'tools',
            'meta_title', 'meta_description',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
