# Generated by Django 3.2.4 on 2024-09-05 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerpoint',
            options={'verbose_name': 'Customer Point', 'verbose_name_plural': 'Customer Points'},
        ),
        migrations.RemoveField(
            model_name='customerpoint',
            name='remaining_point',
        ),
    ]
