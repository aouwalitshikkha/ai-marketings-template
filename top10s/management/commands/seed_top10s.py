from django.core.management.base import BaseCommand
from django.utils.text import slugify
from top10s.models import Profiles, Tool, PlaceholderProfile

PROFILES_DATA = [
    {
        "title": "Top 10 AI Marketing Tools to Supercharge Your Campaigns in 2026",
        "intro": "<p>AI is no longer a futuristic luxury — it's a necessity for modern marketers. After testing 40+ platforms, we've narrowed down the top 10 AI marketing tools that deliver real ROI, automate busywork, and sharpen your strategy.</p>",
        "tldr": "<p>We tested 40+ tools across content creation, analytics, automation, and design. These 10 stood out for ease of use, feature depth, and actual business impact.</p>",
        "conclusion": "<p>AI marketing tools aren't about replacing marketers — they're about amplifying what you already do well. Start with one tool from this list, master it, then expand. The ROI speaks for itself.</p>",
        "meta_title": "Top 10 AI Marketing Tools 2026 — Tested & Ranked",
        "meta_description": "After testing 40+ AI marketing platforms, here are the 10 that deliver real results. In-depth reviews, pros/cons, and comparison table.",
        "comparison_table": {
            "headers": ["Tool", "Best For", "Pricing", "Free Trial"],
            "rows": [
                ["Jasper", "Content Writing", "$49/mo", "7 days"],
                ["HubSpot AI", "CRM & Automation", "From $45/mo", "Yes"],
                ["Canva AI", "Design", "Free / $12.99 Pro", "Yes"],
                ["ChatGPT", "Copy & Ideas", "$20/mo Plus", "Yes"],
                ["Surfer SEO", "SEO Optimization", "$69/mo", "7 days"],
                ["Midjourney", "Image Generation", "$10/mo", "No"],
                ["Perplexity", "Research", "Free / $20 Pro", "Yes"],
                ["Synthesia", "Video Creation", "$29/mo", "Yes"],
                ["Grammarly", "Writing Assistant", "$12/mo", "Yes"],
                ["AdCreative.ai", "Ad Creative", "$29/mo", "7 days"]
            ]
        },
        "tools": [
            {
                "name": "Jasper",
                "description": "<p>Jasper is purpose-built for marketing content. It writes blog posts, social captions, email sequences, and ad copy using brand voice presets. The new Jasper Campaigns feature automates multi-channel content drops.</p>",
                "feature_label": "Key Features",
                "features": "Brand voice presets\nCampaigns for multi-channel content\n50+ copywriting templates\nPlagiarism checker\nIntegrates with Surfer SEO",
                "pros_label": "Pros",
                "pros": "Excellent content quality\nTime-saving campaigns feature\nStrong SEO integration\nIntuitive editor",
                "personal_review": "<p>Jasper is my go-to for long-form content. The brand voice feature alone saves hours of manual editing. It's pricey, but for agencies and content teams, the ROI is clear.</p>",
                "order": 1
            },
            {
                "name": "HubSpot AI",
                "description": "<p>HubSpot's AI layer spans their entire CRM — content assistant, chat summaries, predictive lead scoring, and smart compose for emails. It's not a single tool but an AI upgrade across the platform.</p>",
                "feature_label": "Key Features",
                "features": "AI content assistant\nPredictive lead scoring\nSmart email compose\nChat summary & analysis\nCustom AI workflows",
                "pros_label": "Pros",
                "pros": "Deep CRM integration\nEnterprise-grade\nScalable\nExtensive integrations",
                "personal_review": "<p>HubSpot AI is best for teams already in the HubSpot ecosystem. The predictive scoring is genuinely useful for sales handoff. Not ideal for small teams on a budget.</p>",
                "order": 2
            },
            {
                "name": "Canva AI",
                "description": "<p>Canva's AI features — Magic Studio — include Magic Design, Magic Eraser, Background Remover, and text-to-image. It democratizes design for non-designers without compromising quality.</p>",
                "feature_label": "Key Features",
                "features": "Magic Design (AI layouts)\nMagic Eraser & Edit\nAI image generation\nBackground remover\nBrand templates",
                "pros_label": "Pros",
                "pros": "Extremely easy to use\nGenerous free tier\nTeam collaboration\nConstant AI updates",
                "personal_review": "<p>Canva AI is unbeatable for social media graphics and quick mockups. The Magic Design tool generates professional layouts in seconds. I still use Figma for complex designs, but Canva handles 80% of my daily visual needs.</p>",
                "order": 3
            },
            {
                "name": "ChatGPT (OpenAI)",
                "description": "<p>ChatGPT needs no introduction. For marketers, it's an ideation engine, copy editor, research assistant, and content generator. GPT-4 and custom GPTs make it even more powerful for specific marketing workflows.</p>",
                "feature_label": "Key Features",
                "features": "Conversational AI\nCustom GPTs\nWeb browsing & data analysis\nDALL·E integration\nAPI access",
                "pros_label": "Pros",
                "pros": "Extremely versatile\nFast iteration\nLarge context window\nCustom instructions",
                "personal_review": "<p>ChatGPT is my daily driver for brainstorming and first drafts. The custom GPTs feature lets me create specialized assistants for different marketing channels. It's not a replacement for specialized tools but an essential starting point.</p>",
                "order": 4
            },
            {
                "name": "Surfer SEO",
                "description": "<p>Surfer SEO uses AI to analyze top-ranking pages and provide data-driven content guidelines. It scores your content against SERP leaders and suggests structure, word count, and keyword usage improvements.</p>",
                "feature_label": "Key Features",
                "features": "SERP content analysis\nReal-time content score\nKeyword suggestions\nOutline builder\nIntegration with Jasper",
                "pros_label": "Pros",
                "pros": "Data-backed guidelines\nImproves search rankings\nJasper integration\nClear content score",
                "personal_review": "<p>Surfer SEO took my blog posts from ranking on page 5 to page 1 in 3 months. The content score is addictive — I find myself optimizing until I hit 90+. Essential for content marketers who care about organic traffic.</p>",
                "order": 5
            },
            {
                "name": "Midjourney",
                "description": "<p>Midjourney generates stunning, artistic images from text prompts. It's the gold standard for AI image generation, used by marketers for social media visuals, blog headers, ad creatives, and brand imagery.</p>",
                "feature_label": "Key Features",
                "features": "Text-to-image generation\nStyle customization\nHigh-resolution outputs\nUpscaling & variation\nCommercial license",
                "pros_label": "Pros",
                "pros": "Stunning image quality\nArtistic styles\nActive community\nFast generation",
                "personal_review": "<p>Midjourney produces the most beautiful AI images I've seen. It's trickier to master than DALL·E, but the results are worth the learning curve. I use it for featured images and social media visuals exclusively.</p>",
                "order": 6
            },
            {
                "name": "Perplexity AI",
                "description": "<p>Perplexity is an AI-powered research assistant that provides cited, real-time answers. For marketers, it's invaluable for competitor research, trend analysis, and fact-checking. Pro version adds file uploads and longer context.</p>",
                "feature_label": "Key Features",
                "features": "Real-time web search\nCited sources\nFollow-up questions\nFile upload (Pro)\nCollections & threads",
                "pros_label": "Pros",
                "pros": "Accurate with citations\nGreat for research\nFree tier is generous\nSaves hours of Googling",
                "personal_review": "<p>Perplexity replaced Google for my research workflows. The citations let me verify facts instantly, and the threaded conversations keep complex research organized. The Pro tier is worth it for file uploads alone.</p>",
                "order": 7
            },
            {
                "name": "Synthesia",
                "description": "<p>Synthesia creates AI-generated videos with realistic avatars. Type a script, choose an avatar, and get a professional video in minutes. No camera, no studio, no actors needed.</p>",
                "feature_label": "Key Features",
                "features": "AI avatars (140+)\nText-to-speech (120+ languages)\nScreen recording\nPowerPoint import\nCustom avatar creation",
                "pros_label": "Pros",
                "pros": "No filming required\nQuick turnaround\nProfessional quality\nMultilingual support",
                "personal_review": "<p>Synthesia is a game-changer for explainer videos and internal comms. The avatars are realistic enough for most business use cases. Script-to-video in under 30 minutes — my L&D team loves it.</p>",
                "order": 8
            },
            {
                "name": "Grammarly",
                "description": "<p>Grammarly's AI writing assistant checks grammar, tone, clarity, and engagement. The generative AI features now include full-text rewrites, email composition, and brand-specific style guidance.</p>",
                "feature_label": "Key Features",
                "features": "Grammar & spell check\nTone detection\nGenerative AI rewrite\nBrand style guide\nPlagiarism checker",
                "pros_label": "Pros",
                "pros": "Works everywhere (browser, desktop)\nTone adjustments\nSaves editing time\nTeam admin controls",
                "personal_review": "<p>Grammarly is my safety net. It catches errors I'd miss and helps me adjust tone for different channels. The generative AI rewrite feature is surprisingly good for polishing rough drafts.</p>",
                "order": 9
            },
            {
                "name": "AdCreative.ai",
                "description": "<p>AdCreative.ai generates high-converting ad creatives and social media visuals using AI. It analyzes past campaign data to predict which designs will perform best, integrates with ad platforms, and offers A/B testing suggestions.</p>",
                "feature_label": "Key Features",
                "features": "AI ad creative generation\nPredictive performance scores\nAd platform integrations\nA/B testing suggestions\nCreative analytics",
                "pros_label": "Pros",
                "pros": "Data-driven creative decisions\nSaves design time\nIntegration with Google & Meta\nPerformance prediction",
                "personal_review": "<p>AdCreative.ai transformed our Facebook ad performance. The predictive scoring helps us skip poorly-performing designs before they drain budget. Our CTR improved 34% in the first month.</p>",
                "order": 10
            }
        ]
    },
    {
        "title": "Top 10 Free AI Courses to Learn AI Marketing in 2026",
        "intro": "<p>You don't need a computer science degree to master AI marketing. These 10 free courses — from Google to DeepLearning.AI — teach you how to use AI tools, build prompts, and integrate AI into your marketing workflow.</p>",
        "tldr": "<p>We curated 10 free (or freemium) courses that cover AI fundamentals, prompt engineering, and marketing-specific AI applications. Total cost: $0.</p>",
        "conclusion": "<p>The best investment you can make this year is learning how to work with AI, not against it. These courses give you a practical, hands-on foundation without spending a dime.</p>",
        "meta_title": "Top 10 Free AI Marketing Courses 2026 — Learn AI for Free",
        "meta_description": "10 free AI courses for marketers. Learn prompt engineering, AI content creation, and marketing automation from Google, DeepLearning.AI, and more.",
        "comparison_table": {
            "headers": ["Course", "Platform", "Duration", "Level"],
            "rows": [
                ["AI for Everyone", "DeepLearning.AI", "4 weeks", "Beginner"],
                ["Google AI for Marketers", "Google Skillshop", "2 hours", "Beginner"],
                ["ChatGPT Prompt Engineering", "Vanderbilt/Coursera", "18 hours", "Intermediate"],
                ["Generative AI for Marketing", "LinkedIn Learning", "1.5 hours", "Beginner"],
                ["Hugging Face NLP Course", "Hugging Face", "Self-paced", "Advanced"],
                ["AI in Digital Marketing", "HubSpot Academy", "1 hour", "Beginner"],
                ["Introduction to LLMs", "Google Cloud Skills", "1 week", "Intermediate"],
                ["LangChain for LLM Apps", "FreeCodeCamp", "3 hours", "Advanced"],
                ["Midjourney Masterclass", "YouTube", "2 hours", "Beginner"],
                ["Data Science for Marketing", "Harvard/edX", "8 weeks", "Intermediate"]
            ]
        },
        "tools": [
            {
                "name": "AI for Everyone (DeepLearning.AI)",
                "description": "<p>Andrew Ng's 'AI for Everyone' is the definitive non-technical introduction to AI. It covers what AI can and can't do, how to build AI strategy, and how to navigate ethical challenges. Perfect for marketing leaders.</p>",
                "feature_label": "Key Topics",
                "features": "What AI can and can't do\nBuilding AI strategy\nEthical AI considerations\nCase studies from industry\nTechnical concepts simply explained",
                "pros_label": "Why Take It",
                "pros": "Taught by Andrew Ng\nNon-technical and accessible\nPractical frameworks\nFree certificate option",
                "personal_review": "<p>The best starting point for any marketer. Andrew Ng explains complex AI concepts in plain English. I recommend this to every marketing leader before they invest in AI tools.</p>",
                "order": 1
            },
            {
                "name": "Google AI for Marketers",
                "description": "<p>Google's free Skillshop course teaches marketers how to leverage Google's AI tools — from Performance Max campaigns to AI-powered analytics and content generation. Hands-on, practical, and directly applicable.</p>",
                "feature_label": "Key Topics",
                "features": "Performance Max campaigns\nAI in Google Analytics\nSmart Bidding strategies\nGenerative AI in Ads\nAI-powered content tools",
                "pros_label": "Why Take It",
                "pros": "Official Google training\nDirectly applicable to Google Ads\nShort (2 hours)\nFree certification",
                "personal_review": "<p>Took this in an afternoon and immediately applied the PMax strategies to a client account. Performance improved 22% in two weeks. If you spend money on Google Ads, take this course.</p>",
                "order": 2
            },
            {
                "name": "ChatGPT Prompt Engineering for Developers",
                "description": "<p>Taught by OpenAI and DeepLearning.AI, this course teaches prompt engineering best practices: iterative prompting, chain-of-thought, system messages, and building LLM-powered applications.</p>",
                "feature_label": "Key Topics",
                "features": "Prompt engineering best practices\nChain-of-thought prompting\nSystem vs user messages\nBuilding LLM apps\nIterative prompt development",
                "pros_label": "Why Take It",
                "pros": "From OpenAI itself\nHands-on Jupyter notebooks\nPractical techniques\nShort but dense",
                "personal_review": "<p>This course fundamentally changed how I write prompts. The chain-of-thought technique alone is worth the 18 hours. I now get useful outputs on the first try instead of wrestling with prompts.</p>",
                "order": 3
            },
            {
                "name": "Generative AI for Marketers (LinkedIn Learning)",
                "description": "<p>A concise, practical course covering how marketers can use generative AI for content creation, campaign ideation, personalization, and analytics. Great for busy professionals.</p>",
                "feature_label": "Key Topics",
                "features": "Content generation with AI\nCampaign ideation\nPersonalization at scale\nAI-powered analytics\nEthical considerations",
                "pros_label": "Why Take It",
                "pros": "Concise (1.5 hours)\nMarketer-specific\nPractical examples\nLinkedIn profile badge",
                "personal_review": "<p>Perfect for a lunch break. It won't make you an expert, but it gives a solid overview of what's possible. The personalization section is packed with actionable ideas.</p>",
                "order": 4
            },
            {
                "name": "Hugging Face NLP Course",
                "description": "<p>A deep dive into natural language processing using the Hugging Face ecosystem. Covers transformers, tokenization, fine-tuning, and deployment. For marketers who want to understand how AI processes language.</p>",
                "feature_label": "Key Topics",
                "features": "Transformer architecture\nTokenization & embeddings\nFine-tuning models\nSentiment analysis\nText classification & summarization",
                "pros_label": "Why Take It",
                "pros": "Industry-standard tools\nHands-on coding\nActive community\nFree and comprehensive",
                "personal_review": "<p>This is advanced — you'll need Python basics. But understanding how models actually process text gave me a massive edge in designing prompts and evaluating AI tools. Hugging Face is the industry standard.</p>",
                "order": 5
            }
        ]
    }
]


class Command(BaseCommand):
    help = "Seed demo data for Top 10 lists"

    def handle(self, *args, **options):
        created = 0

        for data in PROFILES_DATA:
            tools_data = data.pop("tools")
            slug = slugify(data["title"])

            if Profiles.objects.filter(slug=slug).exists():
                self.stdout.write(f"Skipping existing: {data['title']}")
                continue

            profile = Profiles.objects.create(slug=slug, **data)

            for tool_data in tools_data:
                Tool.objects.create(blog_post=profile, **tool_data)

            PlaceholderProfile.objects.create(
                profile=profile,
                key="cta_text",
                value="Ready to transform your marketing? Start with one tool today.",
            )

            created += 1
            self.stdout.write(f"Created: {profile.title}")

        self.stdout.write(self.style.SUCCESS(f"Done! Created {created} profiles with tools and placeholders."))
