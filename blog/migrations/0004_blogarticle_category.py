# Generated by Django 5.2 on 2025-05-24 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blogarticle_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogarticle',
            name='category',
            field=models.CharField(choices=[('general', 'General'), ('travel', 'Travel'), ('real_estate', 'Real Estate')], default='general', max_length=30),
        ),
    ]
