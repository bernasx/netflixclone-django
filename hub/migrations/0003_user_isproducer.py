# Generated by Django 4.0.4 on 2022-05-21 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0002_user_fullname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isProducer',
            field=models.BooleanField(default=False),
        ),
    ]
