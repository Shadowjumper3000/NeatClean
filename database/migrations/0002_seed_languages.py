from django.db import migrations


def create_languages(apps, schema_editor):
    Language = apps.get_model("database", "Language")
    languages = [
        ("English", "en"),
        ("Spanish", "es"),
        ("French", "fr"),
        ("German", "de"),
        ("Italian", "it"),
        ("Portuguese", "pt"),
        ("Chinese", "zh"),
        ("Japanese", "ja"),
        ("Korean", "ko"),
        ("Russian", "ru"),
    ]
    for name, code in languages:
        Language.objects.create(name=name, code=code)


class Migration(migrations.Migration):
    dependencies = [
        (
            "database",
            "0001_initial",
        ),  # Update this line to point to the initial migration
    ]

    operations = [
        migrations.RunPython(create_languages),
    ]
