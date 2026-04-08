from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import CustomerProfile, ArtisanProfile, Wallet

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'customer':
            CustomerProfile.objects.create(user=instance)
        elif instance.role == 'artisan':
            ArtisanProfile.objects.create(user=instance)
            Wallet.objects.create(artisan=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 'customer':
        if hasattr(instance, 'customerprofile'):
            instance.customerprofile.save()
    elif instance.role == 'artisan':
        if hasattr(instance, 'artisanprofile'):
            instance.artisanprofile.save()