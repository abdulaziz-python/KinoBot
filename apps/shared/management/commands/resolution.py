import csv
from typing import Any

from django.core.management import BaseCommand

from apps.backend.models.resolution import Resolution


class Command(BaseCommand):
    help = "Create a new Resolution object from resolution.csv"

    def handle(self, *args: Any, **options: Any):
        try:
            with open("assets/resources/resolution.csv", mode="r") as file:
                reader = csv.DictReader(file)
                resolutions = [
                    {
                        "name": row["name"],
                        "width": row["width"],
                        "height": row["height"],
                        "bandwidth": row["bandwidth"],
                        "label": row["label"],
                    }
                    for row in reader
                ]

            existing_names = set(
                Resolution.objects.filter(
                    name__in=[r["name"] for r in resolutions]
                ).values_list("name", flat=True)
            )
            new_resolutions = [
                Resolution(**data)
                for data in resolutions
                if data["name"] not in existing_names
            ]
            Resolution.objects.bulk_create(new_resolutions)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {len(new_resolutions)} Resolution objects."
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
