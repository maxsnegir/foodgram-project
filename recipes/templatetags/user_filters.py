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


@register.filter
def tag_format_class(tag):
    value = tag.data.get('value')
    selected = tag.data.get('selected')

    if value == 'BF':
        attrs = {'id': 'id_breakfast',
                 'class': 'tags__checkbox tags__checkbox_style_orange',
                 'checked': selected}
    elif value == 'LH':
        attrs = {'id': 'id_lunch',
                 'class': 'tags__checkbox tags__checkbox_style_green',
                 'checked': selected}
    else:
        attrs = {'id': 'id_dinner',
                 'class': 'tags__checkbox tags__checkbox_style_purple',
                 'checked': selected}
    tag.data['attrs'] = attrs
    return tag
