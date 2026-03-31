from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import CustomUser, ArtisanProfile


@receiver(pre_save, sender=CustomUser)
def sync_is_artisan_with_role(sender, instance, **kwargs):
    """
    Automatically sync is_artisan flag with role field.
    This ensures consistency between role='artisan' and is_artisan=True
    """
    if instance.role == 'artisan':
        instance.is_artisan = True
    else:
        instance.is_artisan = False


@receiver(post_save, sender=CustomUser)
def create_or_update_artisan_profile(sender, instance, created, **kwargs):
    """
    Create or update ArtisanProfile when a user is created or updated.
    If the user is an artisan, ensure they have an ArtisanProfile.
    """
    if instance.is_artisan:
        # Create ArtisanProfile if it doesn't exist
        ArtisanProfile.objects.get_or_create(user=instance)
    else:
        # Delete ArtisanProfile if user is no longer an artisan
        ArtisanProfile.objects.filter(user=instance).delete()
