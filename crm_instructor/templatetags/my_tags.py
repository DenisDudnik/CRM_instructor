from django import template

register = template.Library()


@register.filter()
def cut_string(text):
    limit = 80
    if len(text) <= limit:
        return text
    cut_text = text[:limit]
    last_space = cut_text.rfind(' ')
    return f'{cut_text[:last_space]}...'
