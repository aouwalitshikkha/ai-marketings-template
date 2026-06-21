from django.db import migrations
from django.utils.text import slugify


def seed_demo_data(apps, schema_editor):
    GlossaryTerm = apps.get_model('glossary', 'GlossaryTerm')

    terms = [
        {
            'term': 'AI Marketing',
            'slug': 'ai-marketing',
            'short_definition': 'The use of artificial intelligence technologies — such as machine learning, natural language processing, and generative AI — to automate, optimize, and personalize marketing activities.',
            'long_definition': 'Encompasses content creation, audience targeting, predictive analytics, and campaign management.',
        },
        {
            'term': 'ChatGPT',
            'slug': 'chatgpt',
            'short_definition': 'A conversational AI model developed by OpenAI that generates human-like text responses.',
            'long_definition': 'Widely used by marketers for content ideation, copywriting, audience research, email drafting, and brainstorming. The GPT-4o model offers real-time web search, file analysis, and multi-turn conversations.',
        },
        {
            'term': 'Generative AI',
            'slug': 'generative-ai',
            'acronym': 'GenAI',
            'short_definition': 'A subset of artificial intelligence that creates new content — text, images, audio, video, or code — based on patterns learned from training data.',
            'long_definition': 'Tools like ChatGPT (text), Midjourney (images), and Adobe Firefly (design) fall under this category. For marketers, GenAI enables rapid content production at scale.',
        },
        {
            'term': 'Large Language Model',
            'slug': 'large-language-model',
            'acronym': 'LLM',
            'short_definition': 'A type of AI model trained on vast amounts of text data to understand and generate human language.',
            'long_definition': 'LLMs power tools like ChatGPT, Jasper, and GrammarlyGO. They excel at tasks such as summarization, translation, question answering, and content generation by predicting the next most likely word in a sequence.',
        },
        {
            'term': 'Natural Language Processing',
            'slug': 'natural-language-processing',
            'acronym': 'NLP',
            'short_definition': 'A branch of AI that enables computers to understand, interpret, and generate human language.',
            'long_definition': 'NLP is the underlying technology behind chatbots, sentiment analysis tools, content summarizers, and voice assistants. In marketing, it is used for analyzing customer feedback, automating responses, and optimizing ad copy.',
        },
        {
            'term': 'Prompt Engineering',
            'slug': 'prompt-engineering',
            'short_definition': 'The practice of carefully crafting input instructions (prompts) to guide AI models toward desired outputs.',
            'long_definition': 'Effective prompt engineering involves specifying tone, audience, format, constraints, and examples. Techniques include chain-of-thought prompting, persona prompting, and few-shot learning.',
        },
        {
            'term': 'Predictive Analytics',
            'slug': 'predictive-analytics',
            'short_definition': 'The use of data, statistical algorithms, and machine learning to identify the likelihood of future outcomes based on historical data.',
            'long_definition': 'In marketing, it powers customer lifetime value prediction, churn risk scoring, lead scoring, and personalized product recommendations.',
        },
        {
            'term': 'Retrieval-Augmented Generation',
            'slug': 'retrieval-augmented-generation',
            'acronym': 'RAG',
            'short_definition': 'A technique that combines information retrieval with text generation.',
            'long_definition': 'Instead of relying solely on an LLM internal knowledge, RAG fetches relevant information from an external knowledge base before generating a response. This improves accuracy and enables AI tools to answer questions about proprietary or up-to-date information.',
        },
        {
            'term': 'Sentiment Analysis',
            'slug': 'sentiment-analysis',
            'short_definition': 'An NLP technique that uses AI to determine the emotional tone behind a piece of text — positive, negative, or neutral.',
            'long_definition': 'Marketers use sentiment analysis to monitor brand perception on social media, analyze customer reviews, gauge campaign reception, and identify emerging PR issues before they escalate.',
        },
        {
            'term': 'Zero-Party Data',
            'slug': 'zero-party-data',
            'short_definition': 'Data that customers intentionally and proactively share with a brand — such as preferences, purchase intentions, personal context, and feedback.',
            'long_definition': 'Unlike third-party data, it is collected with explicit consent and is highly accurate. AI tools help marketers analyze zero-party data to deliver hyper-personalized experiences.',
        },
    ]

    for data in terms:
        GlossaryTerm.objects.create(
            term=data['term'],
            slug=data['slug'],
            short_definition=data['short_definition'],
            long_definition=data.get('long_definition', ''),
            acronym=data.get('acronym', ''),
            status='PUBLISHED',
            review_score=100,
        )


def remove_demo_data(apps, schema_editor):
    GlossaryTerm = apps.get_model('glossary', 'GlossaryTerm')
    GlossaryTerm.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_demo_data, remove_demo_data),
    ]
