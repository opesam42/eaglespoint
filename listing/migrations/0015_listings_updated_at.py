# Generated by Django 5.2 on 2025-05-24 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0014_alter_listings_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
