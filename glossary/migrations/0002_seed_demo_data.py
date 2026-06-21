from django.db import migrations


def seed_demo_data(apps, schema_editor):
    GlossaryTerm = apps.get_model('glossary', 'GlossaryTerm')

    terms = [
        {
            'term': 'AI Marketing',
            'short_definition': 'The use of artificial intelligence technologies — such as machine learning, natural language processing, and generative AI — to automate, optimize, and personalize marketing activities.',
            'long_definition': 'Encompasses content creation, audience targeting, predictive analytics, and campaign management.',
        },
        {
            'term': 'ChatGPT',
            'short_definition': 'A conversational AI model developed by OpenAI that generates human-like text responses.',
            'long_definition': 'Widely used by marketers for content ideation, copywriting, audience research, email drafting, and brainstorming.',
        },
        {
            'term': 'Generative AI',
            'acronym': 'GenAI',
            'short_definition': 'A subset of artificial intelligence that creates new content — text, images, audio, video, or code — based on patterns learned from training data.',
            'long_definition': 'Tools like ChatGPT (text), Midjourney (images), and Adobe Firefly (design) fall under this category.',
        },
        {
            'term': 'Large Language Model',
            'acronym': 'LLM',
            'short_definition': 'A type of AI model trained on vast amounts of text data to understand and generate human language.',
            'long_definition': 'LLMs power tools like ChatGPT, Jasper, and GrammarlyGO.',
        },
        {
            'term': 'Natural Language Processing',
            'acronym': 'NLP',
            'short_definition': 'A branch of AI that enables computers to understand, interpret, and generate human language.',
            'long_definition': 'NLP powers chatbots, sentiment analysis, content summarizers, and voice assistants.',
        },
        {
            'term': 'Prompt Engineering',
            'short_definition': 'The practice of carefully crafting input instructions (prompts) to guide AI models toward desired outputs.',
            'long_definition': 'Techniques include chain-of-thought prompting, persona prompting, and few-shot learning.',
        },
        {
            'term': 'Predictive Analytics',
            'short_definition': 'The use of data, statistical algorithms, and machine learning to identify the likelihood of future outcomes based on historical data.',
            'long_definition': 'Powers customer lifetime value prediction, churn risk scoring, and lead scoring.',
        },
        {
            'term': 'Retrieval-Augmented Generation',
            'acronym': 'RAG',
            'short_definition': 'A technique that combines information retrieval with text generation.',
            'long_definition': 'RAG fetches relevant information from an external knowledge base before generating a response.',
        },
        {
            'term': 'Sentiment Analysis',
            'short_definition': 'An NLP technique that uses AI to determine the emotional tone behind text.',
            'long_definition': 'Used to monitor brand perception, analyze reviews, and gauge campaign reception.',
        },
        {
            'term': 'Zero-Party Data',
            'short_definition': 'Data that customers intentionally and proactively share with a brand.',
            'long_definition': 'Collected with explicit consent and used for hyper-personalized experiences.',
        },
    ]

    for data in terms:
        GlossaryTerm.objects.create(
            term=data['term'],
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
