import json
from django import template
from django.utils.html import strip_tags

register = template.Library()


@register.filter
def read_time(value):
    words_per_minute = 200
    word_count = len(value.split())
    minutes = max(1, round(word_count / words_per_minute))
    return minutes


@register.filter
def post_json_ld(post, request):
    try:
        return json.dumps(post.to_jsonld(request), ensure_ascii=False)
    except Exception:
        return "{}"


@register.filter
def faq_json_ld(faqs):
    entities = [
        {
            "@type": "Question",
            "name": faq.question,
            "acceptedAnswer": {"@type": "Answer", "text": strip_tags(faq.answer)},
        }
        for faq in faqs
    ]
    return json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
        ensure_ascii=False,
    )
