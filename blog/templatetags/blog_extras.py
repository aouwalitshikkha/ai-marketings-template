from django import template

register = template.Library()

@register.filter
def read_time(value):
    words_per_minute = 200
    word_count = len(value.split())
    minutes = max(1, round(word_count / words_per_minute))
    return minutes
