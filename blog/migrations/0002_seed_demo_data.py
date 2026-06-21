from django.db import migrations
from django.utils import timezone
from django.utils.text import slugify


def seed_demo_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Category = apps.get_model('blog', 'Category')
    Tag = apps.get_model('blog', 'Tag')
    Post = apps.get_model('blog', 'Post')

    # Get or create superuser (already exists from glossary migration)
    user, _ = User.objects.get_or_create(
        username='aouwal',
        defaults={'is_staff': True, 'is_superuser': True}
    )

    # --- Categories ---
    categories = [
        ('AI Marketing', 'AI-powered marketing strategies and tools.'),
        ('Technology', 'Latest tech trends and web development.'),
        ('Design', 'UI/UX design principles and tools.'),
        ('SEO', 'Search engine optimization tips and tactics.'),
        ('Business', 'Business growth and entrepreneurship.'),
    ]
    for name, desc in categories:
        Category.objects.get_or_create(
            name=name,
            defaults={'slug': slugify(name), 'description': desc, 'indexable': True}
        )

    # --- Tags ---
    tag_names = ['AI', 'CSS', 'Tailwind', 'Productivity', 'SEO', 'Design', 'Marketing', 'Analytics']
    for name in tag_names:
        Tag.objects.get_or_create(name=name, defaults={'slug': slugify(name), 'indexable': True})

    # --- Posts ---
    cat_map = {c.name: c for c in Category.objects.all()}
    tag_map = {t.name: t for t in Tag.objects.all()}
    now = timezone.now()

    posts = [
        {
            'title': 'The Pros of Tailwind CSS',
            'slug': 'pros-of-tailwind-css',
            'category': 'Technology',
            'tags': ['CSS', 'Tailwind'],
            'short_answer': 'Discover how Tailwind CSS is reshaping modern web development and why developers are making the switch.',
            'body': """
<p>When Tailwind CSS first appeared, the developer community was divided. Some loved the utility-first approach; others dismissed it as "inline styles with extra steps." After shipping several production applications with Tailwind, it's clear which camp has the stronger argument.</p>

<h2>What Makes Tailwind Different?</h2>
<p>Unlike traditional CSS frameworks such as Bootstrap or Foundation, Tailwind doesn't provide pre-built components. Instead, it gives you low-level utility classes that you compose directly in your HTML. This fundamental shift changes how you think about styling entirely.</p>

<h2>Speed of Development</h2>
<p>The single biggest advantage of Tailwind is development speed. No context switching between HTML and CSS files, no naming things, and instant feedback when you change a class.</p>
            """,
        },
        {
            'title': 'AI-Powered Content Strategy for 2026',
            'slug': 'ai-powered-content-strategy-2026',
            'category': 'AI Marketing',
            'tags': ['AI', 'Marketing'],
            'short_answer': 'Learn how AI tools can transform your content strategy from ideation to distribution.',
            'body': """
<p>Content marketing in 2026 is being transformed by artificial intelligence. From generating blog post ideas to optimizing headlines for search, AI tools are becoming indispensable for marketers.</p>

<h2>Content Ideation at Scale</h2>
<p>Tools like ChatGPT and Jasper can generate hundreds of content ideas in seconds. The key is learning how to prompt them effectively for your specific audience and niche.</p>

<h2>Automated Content Creation</h2>
<p>AI writing assistants can now produce first drafts of blog posts, social media updates, and email sequences that require minimal editing. This frees up marketers to focus on strategy and refinement.</p>
            """,
        },
        {
            'title': 'Top SEO Trends to Watch This Year',
            'slug': 'top-seo-trends',
            'category': 'SEO',
            'tags': ['SEO', 'Marketing', 'Analytics'],
            'short_answer': 'Stay ahead of the curve with the latest SEO trends that matter for your business.',
            'body': """
<p>Search engine optimization continues to evolve at a rapid pace. Here are the key trends shaping SEO in 2026.</p>

<h2>AI Overviews in Search</h2>
<p>Google's AI-powered search features are changing how users interact with search results. Optimizing for AI overviews requires a focus on clear, authoritative content.</p>

<h2>Core Web Vitals Matter More Than Ever</h2>
<p>With Google's emphasis on user experience, Core Web Vitals have become critical ranking factors. Pages must load quickly, be visually stable, and respond instantly to user interactions.</p>
            """,
        },
        {
            'title': 'Minimalist Design Principles for Modern Interfaces',
            'slug': 'minimalist-design-principles',
            'category': 'Design',
            'tags': ['Design', 'Productivity'],
            'short_answer': 'Exploring the core principles of minimalist design and how they apply to modern interfaces.',
            'body': """
<p>Minimalist design is more than just white space. It is a philosophy that prioritizes content and functionality over decorative elements.</p>

<h2>Less is More</h2>
<p>The principle of "less is more" applies to every aspect of interface design. Fewer colors, fewer fonts, and fewer elements create a cleaner, more focused user experience.</p>
            """,
        },
        {
            'title': 'Bootstrapping vs Venture Capital: What Founders Need to Know',
            'slug': 'bootstrapping-vs-venture-capital',
            'category': 'Business',
            'tags': ['Business', 'Productivity'],
            'short_answer': 'An honest look at the tradeoffs between bootstrapping your startup and pursuing venture funding.',
            'body': """
<p>One of the biggest decisions founders face is how to fund their startup. Both bootstrapping and venture capital have their advantages and tradeoffs.</p>

<h2>The Bootstrap Advantage</h2>
<p>Bootstrapping means maintaining full control over your company. You make decisions based on what is best for your business, not what investors want.</p>

<h2>When VC Makes Sense</h2>
<p>Venture capital can accelerate growth in ways that bootstrapping cannot match. If you are in a winner-take-all market, VC funding might be essential.</p>
            """,
        },
    ]

    for i, data in enumerate(posts):
        cat = cat_map.get(data['category'])
        post = Post.objects.create(
            title=data['title'],
            slug=data['slug'],
            author=user,
            body=data['body'],
            short_answer=data['short_answer'],
            category=cat,
            status='PB',
            publish_date=now - timezone.timedelta(days=i * 3),
        )
        for tag_name in data['tags']:
            tag = tag_map.get(tag_name)
            if tag:
                post.tags.add(tag)


def remove_demo_data(apps, schema_editor):
    Post = apps.get_model('blog', 'Post')
    Category = apps.get_model('blog', 'Category')
    Tag = apps.get_model('blog', 'Tag')
    Post.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_demo_data, remove_demo_data),
    ]
