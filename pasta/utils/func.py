from pytils.translit import slugify
import random

def unique_slugify(instance, title=None, slug=None):
    if not slug:
        if not title:
            title = instance.title
        slug = slugify(title)
        if not instance.__class__.objects.filter(slug=slug).exists():
            return slug
    new_slug = f'{slug}-{random.randrange(1000, 10000)}'
    if instance.__class__.objects.filter(slug=new_slug).exists():
        new_slug = unique_slugify(instance, slug=slug)
    return new_slug

def get_model_dict(model_objs):
    data = []
    for obj in model_objs:
        data.append({
            field: obj.get(field)
            for field in obj.fields
        })