# Generated by Django 5.1.5 on 2025-03-27 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0011_alter_subscribechannel_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="settings",
            name="label_en",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Label"
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="label_ru",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Label"
            ),
        ),
        migrations.AddField(
            model_name="settings",
            name="label_uz",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="Label"
            ),
        ),
    ]
