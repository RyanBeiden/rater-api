# Generated by Django 3.1.3 on 2020-11-21 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import gamerraterapi.models.game


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=25)),
                ('description', models.CharField(max_length=250)),
                ('designer', models.CharField(max_length=25)),
                ('year_released', models.DateField()),
                ('est_time_to_play', models.IntegerField()),
                ('age_rec', models.IntegerField()),
                ('image_url', models.ImageField(blank=True, upload_to=gamerraterapi.models.game.Game.upload_to, verbose_name='Game Image')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', related_query_name='game', to='gamerraterapi.category')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', related_query_name='review', to='gamerraterapi.game')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='player_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', related_query_name='game', to='gamerraterapi.player'),
        ),
    ]
