# Generated by Django 4.0.5 on 2023-02-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fauna', '0010_animalstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='its_alive',
            field=models.BooleanField(default=False),
        ),
    ]
