from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from django.core.exceptions import ValidationError
import magic


def user_directory_path(instance, filename):
    # Get the file extension
    ext = filename.split(".")[-1]
    # Path will be: profile_pictures/customer/1.png or profile_pictures/staff/1.png
    return f"profile_pictures/{instance.user_type}/{instance.id}.{ext}"


def validate_image_file(value):

    valid_types = ["image/jpeg", "image/png", "image/gif"]
    file_type = magic.from_buffer(value.read(1024), mime=True)
    if file_type not in valid_types:
        raise ValidationError("Unsupported file type.")
    value.seek(0)


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(
        max_length=2, unique=True, help_text="ISO 639-1 language code"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


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
        validators=[validate_image_file],
    )
    user_type = models.CharField(
        max_length=20,
        choices=[("customer", "Customer"), ("staff", "Staff")],
        default="customer",
        help_text="Type of user (e.g., Customer or Staff)",
    )
    languages = models.ManyToManyField(
        Language,
        blank=True,
        help_text="Languages spoken by the staff member",
        related_name="speakers",
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
    rating = models.FloatField(default=0.0)

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


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bookings_as_customer"
    )
    staff = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bookings_as_staff"
    )
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        return f"Booking {self.id}: {self.customer} with {self.staff} on {self.date} at {self.time}"

    @staticmethod
    def get_pending_bookings(staff_id):
        return Booking.objects.filter(staff_id=staff_id, status="pending").order_by(
            "date", "time"
        )
