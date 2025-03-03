from django.contrib import admin
from .models import Language, Zipcode, Profile

admin.site.register(Language)
admin.site.register(Zipcode)
admin.site.register(Profile)