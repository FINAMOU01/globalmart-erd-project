from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import CustomUser


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
