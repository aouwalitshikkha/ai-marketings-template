from django.db import migrations


def seed_demo_data(apps, schema_editor):
    GlossaryTerm = apps.get_model('glossary', 'GlossaryTerm')

    terms = [
        ('AI Marketing', 'The use of artificial intelligence technologies — such as machine learning, natural language processing, and generative AI — to automate, optimize, and personalize marketing activities.'),
        ('ChatGPT', 'A conversational AI model developed by OpenAI that generates human-like text responses. Widely used by marketers for content ideation, copywriting, audience research, email drafting, and brainstorming.'),
        ('Generative AI', 'A subset of artificial intelligence that creates new content — text, images, audio, video, or code — based on patterns learned from training data. Tools like ChatGPT (text), Midjourney (images), and Adobe Firefly (design) fall under this category.'),
        ('Large Language Model', 'A type of AI model trained on vast amounts of text data to understand and generate human language. LLMs power tools like ChatGPT, Jasper, and GrammarlyGO.'),
        ('Natural Language Processing', 'A branch of AI that enables computers to understand, interpret, and generate human language. NLP powers chatbots, sentiment analysis, content summarizers, and voice assistants.'),
        ('Prompt Engineering', 'The practice of carefully crafting input instructions (prompts) to guide AI models toward desired outputs. Techniques include chain-of-thought prompting, persona prompting, and few-shot learning.'),
        ('Predictive Analytics', 'The use of data, statistical algorithms, and machine learning to identify the likelihood of future outcomes based on historical data.'),
        ('Retrieval-Augmented Generation', 'A technique that combines information retrieval with text generation. RAG fetches relevant information from an external knowledge base before generating a response.'),
        ('Sentiment Analysis', 'An NLP technique that uses AI to determine the emotional tone behind text. Used to monitor brand perception, analyze reviews, and gauge campaign reception.'),
        ('Zero-Party Data', 'Data that customers intentionally and proactively share with a brand. Collected with explicit consent and used for hyper-personalized experiences.'),
    ]

    for term, desc in terms:
        GlossaryTerm.objects.create(term=term, description=desc, status='PUBLISHED')


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
