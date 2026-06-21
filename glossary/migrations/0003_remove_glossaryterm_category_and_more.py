from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('glossary', '0002_seed_demo_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='glossaryterm',
            name='category',
        ),
        migrations.DeleteModel(
            name='GlossaryCategory',
        ),
    ]
