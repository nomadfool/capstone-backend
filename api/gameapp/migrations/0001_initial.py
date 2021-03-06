# Generated by Django 2.2 on 2019-04-16 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('min_player', models.IntegerField(default=2)),
                ('max_player', models.IntegerField(default=2)),
                ('play_time', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(blank=True, default=2, null=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('area', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('game_status', models.CharField(max_length=100)),
                ('game_location', models.CharField(max_length=100)),
                ('game', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gameapp.Game')),
                ('host', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('play_as', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
                ('player', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('table', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='gameapp.Table')),
            ],
        ),
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=1)),
                ('friend', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='player_friend', to='gameapp.UserProfile')),
                ('player', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='main_player', to='gameapp.UserProfile')),
            ],
        ),
    ]
