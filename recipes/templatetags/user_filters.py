from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
def format_style(tag):
    span = '<span class="badge badge_style_'
    if tag == 'Завтрак':
        span += 'orange">'
    elif tag == 'Обед':
        span += 'green">'
    else:
        span += 'purple">'
    return mark_safe(span + tag + '</span>')


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={'class': css, })
