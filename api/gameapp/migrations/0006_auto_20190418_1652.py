# Generated by Django 2.2 on 2019-04-18 16:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gameapp', '0005_auto_20190418_0534'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='player',
            unique_together={('table', 'player')},
        ),
    ]
