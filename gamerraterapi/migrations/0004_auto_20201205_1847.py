# Generated by Django 3.1.3 on 2020-12-05 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamerraterapi', '0003_auto_20201204_2245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='categories',
        ),
        migrations.AddField(
            model_name='game',
            name='categories',
            field=models.ManyToManyField(to='gamerraterapi.Category'),
        ),
    ]