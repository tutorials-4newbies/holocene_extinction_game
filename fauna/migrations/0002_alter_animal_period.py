# Generated by Django 4.0.5 on 2022-06-22 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fauna', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='period',
            field=models.CharField(choices=[('PERMIAN', 'Permian'), ('TRIASSIC', 'Triassic'), ('JURASSIC', 'Jurassic'), ('CRETACEOUS', 'Cretaceous'), ('PALEOGENE', 'Paleogene'), ('NEOGENE', 'Neogene'), ('QUATERNARY', 'Quaternary')], max_length=50),
        ),
    ]