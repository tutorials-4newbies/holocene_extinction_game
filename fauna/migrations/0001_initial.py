# Generated by Django 4.0.5 on 2022-06-22 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('extinction', models.CharField(max_length=50)),
                ('period', models.CharField(max_length=50)),
                ('taxonomy_class', models.CharField(max_length=50)),
                ('taxonomy_order', models.CharField(max_length=50)),
                ('taxonomy_family', models.CharField(max_length=50)),
            ],
        ),
    ]
