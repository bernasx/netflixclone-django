# Generated by Django 4.0.4 on 2022-05-22 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0008_video_video_alter_view_date_videobanner_thumbnail_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follower',
        ),
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
        migrations.AlterField(
            model_name='tag',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.video'),
        ),
    ]