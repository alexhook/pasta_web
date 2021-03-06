from django.http import HttpRequest
from pytils.translit import slugify
from django.conf import settings 
import random

def unique_slugify(instance, field='title', slug=None, queryset=None, l=settings.SLUGIFY_DEFAULT_PREFIX_LEN):
    if not slug:
        slug = slugify(getattr(instance, field))
    if not queryset:
        queryset = instance.__class__.objects.filter(slug__regex=rf'^{slug}(-\d+)?$')
        if not queryset.filter(slug=slug).exists():
            return slug
        queryset = set(x.slug.replace(f'{slug}-', '') for x in queryset)
    if len([x for x in queryset if len(x) == l]) == 10**l:
        slug = unique_slugify(instance, field, slug, queryset, l+1)
    else:
        a = set(str(x) for x in range((10**(l-1) if l > 1 else 0), 10**l))
        a -= queryset
        slug += f'-{random.choice(list(a))}'
    return slug

def both(arg1, arg2):
    return (arg1 and arg2) or (not arg1 and not arg2)

def is_ajax(request: HttpRequest):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'