# entrepreneurship/models.py

from django.db import models


class Language(models.Model):
    language = models.CharField(max_length=45)

    def __str__(self):
        return self.language


class Zipcode(models.Model):
    zipcode = models.CharField(max_length=45)

    def __str__(self):
        return self.zipcode


class Customer(models.Model):
    surname = models.CharField(max_length=45, null=True, blank=True)
    name = models.CharField(max_length=45, null=True, blank=True)
    email = models.EmailField(max_length=45, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.CharField(max_length=45, null=True, blank=True)
    zipcode = models.ForeignKey(
        Zipcode, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} {self.surname}"


class Staff(models.Model):
    surname = models.CharField(max_length=45, null=True, blank=True)
    name = models.CharField(max_length=45, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, null=True, blank=True
    )
    zipcode = models.ForeignKey(
        Zipcode, on_delete=models.CASCADE, null=True, blank=True
    )
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
