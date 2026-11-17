from django.db.models import FileField, ImageField
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from . import revalidate
from .images import build_renditions, delete_with_renditions


def _image_fields(instance):
    return [f for f in instance._meta.get_fields() if isinstance(f, ImageField)]


def _file_fields(instance):
    return [f for f in instance._meta.get_fields() if isinstance(f, FileField)]


@receiver(pre_save)
def remember_previous_files(sender, instance, **kwargs):
    """Note which stored files a save replaces, so they can be removed after."""
    if not instance.pk or not _file_fields(instance):
        return
    previous = sender._default_manager.filter(pk=instance.pk).first()
    if previous is None:
        return
    instance._replaced_files = [
        (getattr(previous, f.attname), f)
        for f in _file_fields(instance)
        if getattr(previous, f.attname) and getattr(previous, f.attname).name != getattr(instance, f.attname).name
    ]


@receiver(post_save)
def after_save(sender, instance, **kwargs):
    for fieldfile, _field in getattr(instance, "_replaced_files", []):
        delete_with_renditions(fieldfile.name, fieldfile.storage)
    instance._replaced_files = []

    for field in _image_fields(instance):
        fieldfile = getattr(instance, field.attname)
        if fieldfile:
            build_renditions(fieldfile)

    revalidate.queue(getattr(instance, "cache_tags", ()))


@receiver(post_delete)
def after_delete(sender, instance, **kwargs):
    for field in _file_fields(instance):
        fieldfile = getattr(instance, field.attname)
        if fieldfile:
            delete_with_renditions(fieldfile.name, fieldfile.storage)
    revalidate.queue(getattr(instance, "cache_tags", ()))
