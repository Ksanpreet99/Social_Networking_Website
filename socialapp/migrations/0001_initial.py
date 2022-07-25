# Generated by Django 4.0.3 on 2022-04-08 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='profile_photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(default='default.png', null=True, upload_to='Files/pics')),
                ('cover_photo', models.ImageField(default='defaultcover.jpg', null=True, upload_to='Files/pics')),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('phone_no', models.CharField(max_length=15)),
                ('DOB', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='Male', max_length=3)),
                ('city', models.CharField(max_length=20)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('about_me', models.CharField(max_length=150)),
                ('graduate', models.BooleanField(default=False, null=True)),
                ('post_graduate', models.BooleanField(default=False, null=True)),
                ('study_at', models.CharField(max_length=20, null=True)),
                ('work_at', models.CharField(max_length=20, null=True)),
                ('work_city', models.CharField(max_length=20, null=True)),
                ('work_country', django_countries.fields.CountryField(max_length=2, null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_on', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]