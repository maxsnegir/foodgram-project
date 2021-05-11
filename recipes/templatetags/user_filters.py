from django import template
from django.utils.safestring import mark_safe

from users.models import Follow

register = template.Library()


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={'class': css, })


@register.filter
def tag_format_class(tag):
    style = tag.data.get('value').instance.style
    selected = tag.data.get('selected')

    attrs = {'id': 'id_breakfast',
             'class': f'tags__checkbox tags__checkbox_style_{style}',
             'checked': selected
             }

    tag.data['attrs'] = attrs
    return tag


@register.filter
def is_follow(author, user):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter
def tags_filter(request, tag):
    styles = {
        'BF': 'orange',
        'LH': 'green',
        'DR': 'purple'
    }

    class_ = f'class="tags__checkbox tags__checkbox_style_{styles[tag]}'
    active = ''
    url = '?tags='
    # href = url + tag
    tags = request.GET.getlist('tags')
    if tags:
        print('LH' in tags[0].split(','))

    print(tags)
    r = request.GET
    href = r.urlencode()

    a = f'<a id="{tag} class="{class_} {active}" href="?{href}"></a>'
    return mark_safe(a)
