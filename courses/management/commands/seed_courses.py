from django.core.management.base import BaseCommand
from courses.models import CourseCategory, Course, Chapter


CATEGORIES = [
    {
        "name": "ChatGPT & AI Writing",
        "slug": "chatgpt-ai-writing",
        "description": "Learn how to leverage ChatGPT and AI writing tools to create compelling marketing copy, blog posts, and social media content.",
        "icon": "✍️",
        "order": 1,
    },
    {
        "name": "AI Content Strategy",
        "slug": "ai-content-strategy",
        "description": "Master content strategy with AI — from planning and research to optimization and performance tracking.",
        "icon": "📊",
        "order": 2,
    },
    {
        "name": "AI Tools & Automation",
        "slug": "ai-tools-automation",
        "description": "Discover the best AI tools and automation workflows to supercharge your marketing productivity.",
        "icon": "⚡",
        "order": 3,
    },
]

COURSES = [
    {
        "title": "ChatGPT for Marketers",
        "slug": "chatgpt-for-marketers",
        "description": "Learn how to use ChatGPT to write marketing copy, generate content ideas, and automate your workflow.",
        "level": "Beginner",
        "category_slug": "chatgpt-ai-writing",
        "overview": "This comprehensive course covers everything you need to know about using ChatGPT in your marketing efforts.",
        "objectives": "Write compelling email campaigns\nGenerate blog post ideas\nCreate social media content\nAutomate customer responses\nAnalyze campaign performance",
        "requirements": "A free ChatGPT account\nBasic understanding of marketing",
    },
    {
        "title": "Advanced Prompt Engineering",
        "slug": "advanced-prompt-engineering",
        "description": "Master the art of crafting prompts that get you exactly what you need from AI language models.",
        "level": "Advance",
        "category_slug": "chatgpt-ai-writing",
        "overview": "Take your AI writing skills to the next level with advanced prompt engineering techniques.",
        "objectives": "Chain-of-thought prompting\nFew-shot learning techniques\nStructured output formatting\nRole-based prompting\nPrompt chaining workflows",
        "requirements": "Basic ChatGPT experience\nCompleted ChatGPT for Marketers or equivalent",
    },
    {
        "title": "AI-Powered Content Strategy",
        "slug": "ai-powered-content-strategy",
        "description": "Build a complete content strategy powered by AI — from keyword research to performance analysis.",
        "level": "Intermediate",
        "category_slug": "ai-content-strategy",
        "overview": "Learn how to build and execute a content strategy that leverages AI at every stage.",
        "objectives": "AI-driven keyword research\nContent clustering with AI\nAutomated content briefs\nPerformance tracking\nScaling content production",
        "requirements": "Basic SEO knowledge\nFamiliarity with content marketing",
    },
    {
        "title": "SEO Writing with AI",
        "slug": "seo-writing-with-ai",
        "description": "Write SEO-optimized content faster using AI tools while maintaining quality and reader engagement.",
        "level": "Intermediate",
        "category_slug": "ai-content-strategy",
        "overview": "Combine SEO best practices with AI writing to create content that ranks.",
        "objectives": "SEO-friendly AI prompts\nOptimizing AI content for search\nStructuring articles for featured snippets\nInternal linking strategies\nMeasuring content ROI",
        "requirements": "Basic SEO knowledge\nAn AI writing tool account",
    },
    {
        "title": "Marketing Automation with AI",
        "slug": "marketing-automation-with-ai",
        "description": "Automate repetitive marketing tasks using AI tools and build efficient workflows.",
        "level": "Beginner",
        "category_slug": "ai-tools-automation",
        "overview": "Discover how to automate your marketing workflows with AI-powered tools.",
        "objectives": "Email automation workflows\nSocial media scheduling with AI\nLead scoring automation\nChatbot setup and optimization\nAnalytics automation",
        "requirements": "No prior automation experience needed",
    },
    {
        "title": "AI Tools Roundup & Workflows",
        "slug": "ai-tools-roundup",
        "description": "A curated tour of the best AI marketing tools and how to connect them into powerful workflows.",
        "level": "Beginner",
        "category_slug": "ai-tools-automation",
        "overview": "Explore the AI tool landscape and learn how to build connected workflows.",
        "objectives": "Tool evaluation framework\nBuilding connected workflows\nAPI basics for marketers\nNo-code AI integrations\nTool stack optimization",
        "requirements": "None — beginner friendly",
    },
]


class Command(BaseCommand):
    help = "Seed demo CourseCategory and Course data"

    def handle(self, *args, **options):
        cat_map = {}
        for cat_data in CATEGORIES:
            cat, created = CourseCategory.objects.get_or_create(
                slug=cat_data["slug"],
                defaults=cat_data,
            )
            if not created:
                for k, v in cat_data.items():
                    setattr(cat, k, v)
                cat.save()
            cat_map[cat.slug] = cat
        self.stdout.write(f'  Categories: {CourseCategory.objects.count()}')

        for course_data in COURSES:
            slug = course_data["slug"]
            category_slug = course_data["category_slug"]
            fields = {k: v for k, v in course_data.items() if k != "category_slug"}
            fields["course_category"] = cat_map[category_slug]
            course, created = Course.objects.get_or_create(
                slug=slug,
                defaults=fields,
            )
            if not created:
                for k, v in fields.items():
                    setattr(course, k, v)
                course.save()
        self.stdout.write(f'  Courses: {Course.objects.count()}')

        first_course = Course.objects.first()
        if first_course and not first_course.chapters.exists():
            Chapter.objects.create(
                course=first_course,
                number=1,
                title="Getting Started with ChatGPT",
                slug="getting-started",
                summary="An introduction to ChatGPT and how marketers can use it.",
                content="""
<h2>What is ChatGPT?</h2>
<p>ChatGPT is an AI language model developed by OpenAI that can generate human-like text based on prompts.</p>

<h2>Why Marketers Need ChatGPT</h2>
<p>From drafting emails to brainstorming campaign ideas, ChatGPT can save marketers hours of work each week.</p>

<h2>Setting Up Your Account</h2>
<p>Getting started is easy. Visit chat.openai.com, create a free account, and you are ready to go.</p>
""",
                status="published",
            )
            self.stdout.write(f'  Demo chapter created for: {first_course.title}')

        self.stdout.write(self.style.SUCCESS(f'\nDone! {Course.objects.count()} courses across {CourseCategory.objects.count()} categories.'))
