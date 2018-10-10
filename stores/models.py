from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

def create_slug(instance, new_slug=None):
    slug = slugify (instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Store.objects.filter(slug=slug)
    if qs.exists():
        if "-" in slug:
            slug_list = slug.split("-")
            new_slug = "%s-%s"%(slug_list[0],int(slug_list[1])+1)
        else:
            new_slug = "%s-1"%(slug)
        return create_slug(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=Store)
def pre_save_store_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)



