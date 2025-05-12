from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# Signal to create user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Signal to save user profile when user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


class CanteenStatus(models.Model):
    is_open = models.BooleanField(default=False)
    opening_time = models.TimeField(default="09:00:00")
    closing_time = models.TimeField(default="21:00:00")

    def __str__(self):
        return "Open" if self.is_open else "Closed"

