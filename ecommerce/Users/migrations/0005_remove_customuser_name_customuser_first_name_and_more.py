# Generated by Django 5.2.3 on 2025-07-01 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_remove_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='name',
        ),
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
