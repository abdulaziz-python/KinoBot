import csv
from typing import Any

from django.core.management import BaseCommand

from apps.backend.models.settings import Settings


class Command(BaseCommand):
    help = "Create a new Switcher object from switcher.csv"

    def handle(self, *args: Any, **options: Any):
        with open("assets/resources/switcher.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if Settings.objects.filter(key=row["key"]).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            f'Switcher object with key: {row["key"]} already exists. Skipping.'
                        )
                    )
                    continue

                switcher_data = {
                    "key": row["key"],
                    "label_uz": row["label_uz"],
                    "label_ru": row["label_ru"],
                    "label_en": row["label_en"],
                }

                switcher = Settings(**switcher_data)
                switcher.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created Switcher object with key: {row["key"]}'
                    )
                )
