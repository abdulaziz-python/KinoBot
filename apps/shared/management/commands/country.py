import csv
from typing import Any

from django.core.management import BaseCommand

from apps.backend.models.country import Country


class Command(BaseCommand):
    help = "Create a new Country object from countries.csv"

    def handle(self, *args: Any, **options: Any):
        try:
            with open("assets/resources/countries.csv") as file:
                reader = csv.DictReader(file)
                countries = [
                    {
                        "name": row["name"],
                        "native": row["native"],
                        "phone_code": row["phonecode"],
                        "iso2": row["iso2"],
                        "iso3": row["iso3"],
                        "emoji": row["emoji"],
                        "emojiU": row["emojiU"],
                    }
                    for row in reader
                ]
                existing_names = set(
                    Country.objects.filter(
                        iso2__in=[r["iso2"] for r in countries]
                    ).values_list("iso2", flat=True)
                )
                new_resolutions = [
                    Country(**data)
                    for data in countries
                    if data["iso2"] not in existing_names
                ]
                Country.objects.bulk_create(new_resolutions)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully created {len(new_resolutions)} Country objects."
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
