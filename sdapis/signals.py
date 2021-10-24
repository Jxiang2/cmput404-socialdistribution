from .models import Post
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

@receiver(post_save, sender=Post)
def set_source(sender, instance, created, **kwarg):
    if created: 
        print("signal starts working")
        source = instance.source
        origin = instance.origin

        # this is  an original post
        if source == None and origin == None:
            source = instance.get_post_id()
            origin = instance.get_post_id()
            instance.source = source
            instance.origin = origin
            instance.save()

        # this is not an original post
        else:
            #do nothing
            pass