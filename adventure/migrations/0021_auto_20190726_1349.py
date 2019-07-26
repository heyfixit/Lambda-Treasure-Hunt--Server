# Generated by Django 2.2.3 on 2019-07-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0020_auto_20190725_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='vision_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='player',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='cooldown',
            field=models.IntegerField(default=100),
        ),
    ]