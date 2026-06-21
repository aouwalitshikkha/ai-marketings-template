from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import GlossaryTerm
from .views import CACHE_KEY


@receiver([post_save, post_delete], sender=GlossaryTerm)
def clear_glossary_cache(sender, **kwargs):
    cache.delete(CACHE_KEY)
