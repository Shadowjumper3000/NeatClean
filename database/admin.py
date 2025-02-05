# core/admin.py

from django.contrib import admin
from .models import Language, Zipcode, Customer, Staff

admin.site.register(Language)
admin.site.register(Zipcode)
admin.site.register(Customer)
admin.site.register(Staff)
