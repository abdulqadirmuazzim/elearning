from django import template

register = template.Library()


def limit(items, limit):
    return items[:limit]


@register.filter(name="subscript")
def subscript(list, subscript):
    return list[subscript]


register.filter("limit", limit)
