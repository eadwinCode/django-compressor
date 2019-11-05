import os
import six
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def private_static(basename):
    path = os.path.join(settings.BASE_DIR, 'frontend', basename)
    if os.path.exists(path):
        return mark_safe(path)
    raise FileExistsError(f'{path} not found') 