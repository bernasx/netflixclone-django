# Generated by Django 4.0.4 on 2022-05-22 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0012_alter_avatar_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='image',
            field=models.ImageField(blank=True, default='uploads/avatars/default.png', upload_to='uploads/avatars/'),
        ),
    ]