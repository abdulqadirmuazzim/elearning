from django import template

register = template.Library()


def limit(items, limit):
    return items[:limit]


register.filter("limit", limit)
