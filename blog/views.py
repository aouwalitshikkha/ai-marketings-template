from django.db.models import Count
from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag


class BlogHomeView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).select_related('author', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(post_count=Count('posts'))
        context['tags'] = Tag.objects.all()
        context['recent_posts'] = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish_date')[:5]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).select_related('author', 'category').prefetch_related('tags', 'faqs', 'placeholders')


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
        ).select_related('author', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
