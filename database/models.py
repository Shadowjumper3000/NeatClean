from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
    language = models.CharField(max_length=45)

    def __str__(self):
        return self.language


class Zipcode(models.Model):
    zipcode = models.CharField(max_length=45)

    def __str__(self):
        return self.zipcode


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    apartment_door_floor = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, null=True, blank=True
    )
    rating = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username
