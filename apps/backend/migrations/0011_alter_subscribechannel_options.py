# Generated by Django 5.1.5 on 2025-03-27 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("backend", "0010_subscribechannel_channel_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscribechannel",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "Subscribe Channel",
                "verbose_name_plural": "Subscribe Channel",
            },
        ),
    ]
