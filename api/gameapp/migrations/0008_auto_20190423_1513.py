# Generated by Django 2.2 on 2019-04-23 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameapp', '0007_auto_20190419_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='table',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
