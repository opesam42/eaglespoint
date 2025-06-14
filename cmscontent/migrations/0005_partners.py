# Generated by Django 5.2 on 2025-06-03 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmscontent', '0004_teammember_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='partners/')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
