# Generated by Django 4.1.5 on 2023-01-18 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='codregistro',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
