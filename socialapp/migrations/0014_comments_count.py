# Generated by Django 4.0.3 on 2022-04-26 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0013_post_like_alter_profile_is_verified_delete_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='count',
            field=models.IntegerField(blank=True, max_length=2000, null=True),
        ),
    ]
