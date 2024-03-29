# Generated by Django 4.0.5 on 2022-10-19 09:51

from django.db import migrations

dependencies = [
        # ('fauna', '0003_alter_animal_options_animal_creator'),
        # ('django.contrib.auth', '0012_alter_user_first_name_max_length'),
    ]

def set_default_creator(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Animal = apps.get_model('fauna', 'Animal')
    animal_count = Animal.objects.count()
    if animal_count > 0:
        User = apps.get_model("auth", "User")
        default_user = User.objects.filter(is_superuser=True)[0]
        for animal in Animal.objects.all():
            animal.creator = default_user
            animal.save()

def null_default_creator(apps, schema_editor):
    Animal = apps.get_model('fauna', 'Animal')
    animal_count = Animal.objects.count()

    if animal_count > 0:
        for animal in Animal.objects.all():
            animal.creator = None
            animal.save()

class Migration(migrations.Migration):

    dependencies = [
        ('fauna', '0003_alter_animal_options_animal_creator'),
    ]

    operations = [
        migrations.RunPython(set_default_creator, reverse_code=null_default_creator)
    ]


