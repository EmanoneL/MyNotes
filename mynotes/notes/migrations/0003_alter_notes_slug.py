# Generated by Django 5.0.2 on 2024-03-27 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_notes_options_notes_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]