from django.contrib.auth.models import AbstractUser
from django.db import models
import os


def user_directory_path(instance, filename):
    # Get the file extension
    ext = filename.split(".")[-1]
    # Path will be: profile_pictures/customer/1.png or profile_pictures/staff/1.png
    return f"profile_pictures/{instance.user_type}/{instance.id}.{ext}"


class CustomUser(AbstractUser):
    # Personal Information
    phone = models.CharField(
        max_length=15, blank=True, null=True, help_text="User's phone number"
    )
    picture = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        help_text="User's profile picture",
    )
    user_type = models.CharField(
        max_length=20,
        choices=[("customer", "Customer"), ("staff", "Staff")],
        default="customer",
        help_text="Type of user (e.g., Customer or Staff)",
    )

    # Address Information
    street = models.CharField(
        max_length=255, blank=True, null=True, help_text="Street name"
    )
    street_number = models.CharField(
        max_length=20, blank=True, null=True, help_text="Street number"
    )
    apartment = models.CharField(
        max_length=50, blank=True, null=True, help_text="Apartment number"
    )
    city = models.CharField(max_length=100, blank=True, null=True, help_text="City")
    state = models.CharField(
        max_length=100, blank=True, null=True, help_text="State/Province"
    )
    zip_code = models.CharField(
        max_length=20, blank=True, null=True, help_text="ZIP/Postal code"
    )
    country = models.CharField(
        max_length=100, default="United States", help_text="Country"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Delete old picture when updating
        if self.pk:
            try:
                old_instance = CustomUser.objects.get(pk=self.pk)
                if old_instance.picture and self.picture != old_instance.picture:
                    # Delete old picture file
                    if os.path.isfile(old_instance.picture.path):
                        os.remove(old_instance.picture.path)
            except CustomUser.DoesNotExist:
                pass
        super().save(*args, **kwargs)
