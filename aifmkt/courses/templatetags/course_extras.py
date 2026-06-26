from django import template

register = template.Library()


@register.filter
def split(value, sep=","):
    if not value:
        return []
    return [v.strip() for v in value.split(sep)]


@register.filter
def lines_to_list(value):
    if not value:
        return []
    return [line.strip() for line in value.strip().splitlines() if line.strip()]
