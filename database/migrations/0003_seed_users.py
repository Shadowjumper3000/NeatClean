from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_test_users(apps, schema_editor):
    CustomUser = apps.get_model("database", "CustomUser")
    Language = apps.get_model("database", "Language")

    # Create test cleaners
    cleaners = [
        {
            "username": "maria.cleaner",
            "email": "maria@neatclean.com",
            "password": make_password("cleanpass123"),
            "first_name": "Maria",
            "last_name": "Silva",
            "phone": "+1234567890",
            "user_type": "staff",
            "street": "Clean Street",
            "street_number": "42",
            "city": "Cleanville",
            "state": "CA",
            "zip_code": "12345",
            "languages": ["en", "es", "pt"],  # Language codes
        },
        {
            "username": "john.cleaner",
            "email": "john@neatclean.com",
            "password": make_password("cleanpass123"),
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1987654321",
            "user_type": "staff",
            "street": "Mop Avenue",
            "street_number": "15",
            "city": "Cleanville",
            "state": "CA",
            "zip_code": "12345",
            "languages": ["en", "fr", "de"],
        },
    ]

    # Create test clients
    clients = [
        {
            "username": "alice.client",
            "email": "alice@example.com",
            "password": make_password("clientpass123"),
            "first_name": "Alice",
            "last_name": "Johnson",
            "phone": "+1122334455",
            "user_type": "customer",
            "street": "Client Road",
            "street_number": "101",
            "city": "Clientville",
            "state": "CA",
            "zip_code": "54321",
        },
        {
            "username": "bob.client",
            "email": "bob@example.com",
            "password": make_password("clientpass123"),
            "first_name": "Bob",
            "last_name": "Smith",
            "phone": "+1555666777",
            "user_type": "customer",
            "street": "Customer Lane",
            "street_number": "202",
            "city": "Clientville",
            "state": "CA",
            "zip_code": "54321",
        },
    ]

    # Create users and assign languages
    for cleaner_data in cleaners:
        language_codes = cleaner_data.pop("languages")
        cleaner = CustomUser.objects.create(**cleaner_data)
        languages = Language.objects.filter(code__in=language_codes)
        cleaner.languages.set(languages)

    for client_data in clients:
        CustomUser.objects.create(**client_data)


def remove_test_users(apps, schema_editor):
    CustomUser = apps.get_model("database", "CustomUser")
    test_usernames = ["maria.cleaner", "john.cleaner", "alice.client", "bob.client"]
    CustomUser.objects.filter(username__in=test_usernames).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0002_seed_languages"),
    ]

    operations = [
        migrations.RunPython(create_test_users, remove_test_users),
    ]
