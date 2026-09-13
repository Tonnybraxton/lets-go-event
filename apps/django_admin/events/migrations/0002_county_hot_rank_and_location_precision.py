from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models


def populate_known_counties(apps, schema_editor):
    Venue = apps.get_model("events", "Venue")
    city_counties = {
        "Nairobi": "Nairobi",
        "Mombasa": "Mombasa",
        "Kisumu": "Kisumu",
        "Nakuru": "Nakuru",
        "Eldoret": "Uasin Gishu",
        "Kisii": "Kisii",
        "Migori": "Migori",
        "Bomet": "Bomet",
        "Nyeri": "Nyeri",
        "Kitui": "Kitui",
        "Kilifi": "Kilifi",
    }
    for city, county in city_counties.items():
        Venue.objects.filter(city__iexact=city, county="").update(county=county)


class Migration(migrations.Migration):
    dependencies = [("events", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="venue",
            name="county",
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
        migrations.AddField(
            model_name="venue",
            name="coordinates_are_approximate",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Mark this when the source only identifies a town or county rather "
                    "than an exact venue pin."
                ),
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="hot_rank",
            field=models.PositiveSmallIntegerField(
                blank=True,
                help_text="Optional position in the curated Top 10 upcoming Kenya collection.",
                null=True,
                unique=True,
                validators=[MinValueValidator(1), MaxValueValidator(10)],
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="date_confirmed",
            field=models.BooleanField(
                default=True,
                help_text=(
                    "Clear this when a date is corroborated externally but still needs "
                    "organizer confirmation."
                ),
            ),
        ),
        migrations.AddField(
            model_name="event",
            name="time_confirmed",
            field=models.BooleanField(
                default=True,
                help_text=(
                    "Clear this when the source confirms the date but has not published "
                    "a start time."
                ),
            ),
        ),
        migrations.RunPython(populate_known_counties, migrations.RunPython.noop),
    ]
