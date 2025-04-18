# Generated by Django 5.1.5 on 2025-03-25 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cinema",
            name="file_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=255,
                null=True,
                verbose_name="File ID",
            ),
        ),
        migrations.AlterField(
            model_name="channel",
            name="channel_type",
            field=models.CharField(
                choices=[
                    ("TARGET", "Target"),
                    ("SOURCE", "Source"),
                    ("DRAFT", "Draft"),
                ],
                default="SOURCE",
                max_length=50,
                verbose_name="Channel Type",
            ),
        ),
        migrations.AlterField(
            model_name="cinema",
            name="message_id",
            field=models.PositiveBigIntegerField(
                blank=True, db_index=True, null=True, verbose_name="Message ID"
            ),
        ),
    ]
