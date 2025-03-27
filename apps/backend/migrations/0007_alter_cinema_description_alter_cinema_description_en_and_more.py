# Generated by Django 5.1.5 on 2025-03-27 08:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0006_alter_cinema_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cinema",
            name="description",
            field=models.TextField(
                db_index=True,
                validators=[django.core.validators.MaxLengthValidator(600)],
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="cinema",
            name="description_en",
            field=models.TextField(
                db_index=True,
                null=True,
                validators=[django.core.validators.MaxLengthValidator(600)],
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="cinema",
            name="description_ru",
            field=models.TextField(
                db_index=True,
                null=True,
                validators=[django.core.validators.MaxLengthValidator(600)],
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="cinema",
            name="description_uz",
            field=models.TextField(
                db_index=True,
                null=True,
                validators=[django.core.validators.MaxLengthValidator(600)],
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="cinema",
            name="title",
            field=models.CharField(db_index=True, max_length=100, verbose_name="Name"),
        ),
        migrations.AlterField(
            model_name="cinema",
            name="title_en",
            field=models.CharField(
                db_index=True, max_length=100, null=True, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="cinema",
            name="title_ru",
            field=models.CharField(
                db_index=True, max_length=100, null=True, verbose_name="Name"
            ),
        ),
        migrations.AlterField(
            model_name="cinema",
            name="title_uz",
            field=models.CharField(
                db_index=True, max_length=100, null=True, verbose_name="Name"
            ),
        ),
    ]
