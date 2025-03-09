from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    # Link the Profile to the Django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Additional fields
    name = models.CharField(max_length=100, blank=True, null=True, help_text="User's first name")
    surname = models.CharField(max_length=100, blank=True, null=True, help_text="User's last name")
    email = models.EmailField(max_length=100, blank=True, null=True, help_text="User's email address")
    phone = models.CharField(max_length=15, blank=True, null=True, help_text="User's phone number")
    address = models.CharField(max_length=255, blank=True, null=True, help_text="User's address")
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, help_text="User's profile picture")
    user_type = models.CharField(
        max_length=20,
        choices=[('customer', 'Customer'), ('staff', 'Staff')],
        default='customer',
        help_text="Type of user (e.g., Customer or Staff)"
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

# Signal to create or update the Profile when a User is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()