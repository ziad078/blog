from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Comment

@receiver(post_save, sender=Comment)
def update_comments_no(instance, created, **kwargs):
    blog = instance.blog
    if created and instance.active:
        blog.no_of_comments += 1
    elif not created and not instance.active:
        blog.no_of_comments -= 1
    blog.save()

@receiver(post_delete, sender=Comment)
def update_comments_no_delete(instance, **kwargs):
    blog = instance.blog
    if instance.active:
        blog.no_of_comments -= 1
        blog.save()



