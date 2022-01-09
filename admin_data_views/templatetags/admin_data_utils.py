from django import template


register = template.Library()


@register.filter
def get_type(value) -> str:
    return type(value).__name__
