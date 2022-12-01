# Generated by Django 4.0.5 on 2022-11-23 10:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fauna', '0007_animal_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='animals_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
