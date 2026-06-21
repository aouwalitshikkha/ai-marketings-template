import html2text
from django import template
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
