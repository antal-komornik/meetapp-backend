from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserAdditionalInfo
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

# @receiver(post_save, sender=User)
# def create_user_additional_info(sender, instance, created, **kwargs):
#     if created:
#         UserAdditionalInfo.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def create_user_additional_info(sender, instance, created, **kwargs):
    if created:
        UserAdditionalInfo.objects.create(user=instance)