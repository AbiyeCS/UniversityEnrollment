from django import template
register = template.Library()


@register.filter(name='dict_items')
def dict_items(value):
    print(vars(value).items())
    return vars(value).items()