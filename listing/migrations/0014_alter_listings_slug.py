# Generated by Django 5.2 on 2025-05-18 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0013_listings_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='slug',
            field=models.CharField(blank=True, max_length=60, null=True, unique=True),
        ),
    ]
