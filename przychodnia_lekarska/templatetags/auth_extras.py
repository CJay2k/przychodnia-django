from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter(name='get_group')
def get_group(user):
    group = Group.objects.get(name=user)
    return group if group in user.groups.all() else 'Brak'