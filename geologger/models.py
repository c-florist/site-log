from django.contrib.gis.db.models import PointField
from django.db.models import Model, TextField, PositiveIntegerField


class JobSite(Model):
    name = TextField(unique=True)
    address = TextField()
    location = PointField()
    radius_m = PositiveIntegerField(default=50, help_text="Radius of the geofence for this job site in meters.")

    def __str__(self) -> str:
        return self.name
