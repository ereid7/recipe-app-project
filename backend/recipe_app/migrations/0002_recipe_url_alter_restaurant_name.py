# Generated by Django 5.0.3 on 2024-03-13 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='url',
            field=models.URLField(unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
