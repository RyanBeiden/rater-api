# Generated by Django 3.1.3 on 2021-01-22 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamerraterapi', '0006_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='rating',
            new_name='value',
        ),
    ]