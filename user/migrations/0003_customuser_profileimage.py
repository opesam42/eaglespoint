# Generated by Django 5.1.7 on 2025-04-03 23:17

import user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customuser_managers_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profileImage',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.user_directory_path),
        ),
    ]
