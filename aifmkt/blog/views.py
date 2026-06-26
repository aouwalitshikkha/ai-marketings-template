from django.db.models import Count
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.utils.html import strip_tags
from markdownify import markdownify as md
from .models import Post, Category, Tag


class BlogHomeView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).select_related('category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(post_count=Count('posts'))
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-updated_at')[:5]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).select_related('category').prefetch_related('tags', 'faqs', 'placeholders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        if post.category:
            context['related_posts'] = Post.objects.filter(
                status=Post.Status.PUBLISHED,
                category=post.category
            ).select_related('category').exclude(pk=post.pk)[:3]
        else:
            context['related_posts'] = []
        return context


class PostMarkdownView(DetailView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def render_to_response(self, context, **response_kwargs):
        post = self.object
        body_md = md(post.body, heading_style="ATX")
        content = (
            f"---\n"
            f"title: {post.title}\n"
            f"author: Abdul Aouwal\n"
            f"date: {post.updated_at.date()}\n"
            f"slug: {post.slug}\n"
            f"---\n\n"
            f"# {post.title}\n\n"
            f"{body_md}"
        )
        return HttpResponse(content, content_type='text/markdown; charset=utf-8')


class CategoryView(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(
            status=Post.Status.PUBLISHED,
            category=self.category
        ).select_related('category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.annotate(post_count=Count('posts'))
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-updated_at')[:5]
        return context
