from django.db import migrations


def add_ratings(apps, schema_editor):
    CustomUser = apps.get_model("database", "CustomUser")

    # Update cleaners with ratings
    cleaner_ratings = {"maria.cleaner": 4.8, "john.cleaner": 4.5}

    for username, rating in cleaner_ratings.items():
        try:
            cleaner = CustomUser.objects.get(username=username)
            cleaner.rating = rating
            cleaner.save()
        except CustomUser.DoesNotExist:
            pass


def remove_ratings(apps, schema_editor):
    CustomUser = apps.get_model("database", "CustomUser")
    CustomUser.objects.filter(user_type="staff").update(rating=0.0)


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0003_seed_users"),
    ]

    operations = [
        migrations.RunPython(add_ratings, remove_ratings),
    ]
