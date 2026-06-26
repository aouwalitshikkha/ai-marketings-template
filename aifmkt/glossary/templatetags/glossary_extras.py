import json
import html2text
from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()
converter = html2text.HTML2Text()
converter.body_width = 0
converter.ignore_links = False
converter.ignore_images = False


@register.filter
def html_to_md(value):
    if not value:
        return ''
    return mark_safe(converter.handle(str(value)))


@register.filter
def defined_term_set(groups):
    """Build a schema.org DefinedTermSet JSON-LD payload from glossary groups."""
    terms = []
    for group in groups:
        for term in group.get('terms', []):
            terms.append({
                "@type": "DefinedTerm",
                "name": term.term,
                "description": strip_tags(term.description).strip(),
            })
    payload = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "name": "AI Marketing Glossary",
        "hasDefinedTerm": terms,
    }
    return mark_safe(json.dumps(payload, ensure_ascii=False))
