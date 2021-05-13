from django import template
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
def is_selected(request, tag):
    tags = request.GET.getlist('tags')
    if tags:
        return tag in tags
    return True


@register.simple_tag
def tags_links(request, tag, all_tags):
    tags = request.GET.getlist('tags')
    if tags:
        new_request = request.GET.copy()
        if request.GET.getlist('page'):  # Удаляем page
            new_request.pop('page')
        if tag.slug in tags:
            tags.remove(tag.slug)
            new_request.setlist("tags", tags)
        else:
            new_request.appendlist("tags", tag.slug)
        return new_request.urlencode()
    # Если в запросе нет тегов
    result = []
    for t in all_tags:
        if t != tag:  # Выводить все кроме текущего
            result.append('tags=' + t.slug)

    return '&'.join(result)


@register.simple_tag
def add_tags_to_pagination(request, param, value):
    new_request = request.GET.copy()
    new_request[param] = value

    return new_request.urlencode()
